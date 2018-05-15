#!/usr/bin/env python
# Python 2.7.x - 3.6.x
# LinkFinder
# By Gerben_Javado

# Fix webbrowser bug for MacOS
import os
os.environ["BROWSER"] = "open"

# Import libraries
import re, sys, glob, cgi, argparse, jsbeautifier, webbrowser, subprocess, base64, ssl, xml.etree.ElementTree
from string import Template 

try:
    from urllib.request import Request, urlopen
except ImportError:
    from urllib2 import Request, urlopen

# Parse command line
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--domain",
                    help="Input a domain to recursively parse all javascript located in a page",
                    action="store_true")
parser.add_argument("-i", "--input",
                    help="Input a: URL, file or folder. \
                    For folders a wildcard can be used (e.g. '/*.js').",
                    required="True", action="store")
parser.add_argument("-o", "--output",
                    help="Where to save the file, \
                    including file name. Default: output.html",
                    action="store", default="output.html")
parser.add_argument("-r", "--regex",
                    help="RegEx for filtering purposes \
                    against found endpoint (e.g. ^/api/)",
                    action="store")
parser.add_argument("-b", "--burp",
                    help="",
                    action="store_true")
parser.add_argument("-c", "--cookies",
                    help="Add cookies for authenticated JS files",
                    action="store", default="")
args = parser.parse_args()

# Newlines in regex? Important for CLI output without jsbeautifier
if args.output != 'cli':
    addition = ("[^\n]*","[^\n]*")
else:
    addition = ("","")

# Regex used
regex = re.compile(r"""

  (%s(?:"|')                            # Start newline delimiter

  (?:
    ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
    [^"'/]{1,}\.                        # Match a domainname (any character + dot)
    [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path

    |

    ((?:/|\.\./|\./)                    # Start with /,../,./
    [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be... 
    [^"'><,;|()]{1,})                   # Rest of the characters can't be

    |

    ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
    [a-zA-Z0-9_\-/]{1,}\.[a-zA-Z]{1,4}  # Rest + extension
    (?:[\?|/][^"|']{0,}|))              # ? mark with parameters

    |

    ([a-zA-Z0-9_\-]{1,}                 # filename
    \.(?:php|asp|aspx|jsp|json)         # . + extension
    (?:\?[^"|']{0,}|))                  # ? mark with parameters
 
  )             
  
  (?:"|')%s)                            # End newline delimiter

""" % addition, re.VERBOSE)

def parser_error(errmsg):
    '''
    Error Messages
    '''
    print("Usage: python %s [Options] use -h for help" % sys.argv[0])
    print("Error: %s" % errmsg)
    sys.exit()


def parser_input(input):
    '''
    Parse Input
    '''

    # Method 1 - URL
    if input.startswith(('http://', 'https://',
                         'file://', 'ftp://', 'ftps://')):
        return [input]

    # Method 2 - URL Inspector Firefox
    if input.startswith('view-source:'):
        return [input[12:]]

    # Method 3 - Burp file
    if args.burp:
        jsfiles = []
        items = xml.etree.ElementTree.fromstring(open(args.input, "r").read())
        
        for item in items:
            jsfiles.append({"js":base64.b64decode(item.find('response').text).decode('utf-8',"replace"), "url":item.find('url').text})
        return jsfiles

    # Method 4 - Folder with a wildcard
    if "*" in input:
        paths = glob.glob(os.path.abspath(input))
        for index, path in enumerate(paths):
            paths[index] = "file://%s" % path
        return (paths if len(paths) > 0 else parser_error('Input with wildcard does \
        not match any files.'))

    # Method 5 - Local file
    path = "file://%s" % os.path.abspath(input)
    return [path if os.path.exists(input) else parser_error("file could not \
be found (maybe you forgot to add http/https).")]


def send_request(url):
    '''
    Send requests with Requests
    '''
    q = Request(url)
    # Support websites that force TLSv1.2
    sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

    q.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
    q.add_header('Accept', 'text/html,\
        application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    q.add_header('Accept-Language', 'en-US,en;q=0.8')
    q.add_header('Accept-Encoding', '')
    q.add_header('Cookie', args.cookies)

    return urlopen(q, context=sslcontext).read().decode('utf-8', 'replace')

def parser_file(content):
    '''
    Parse Input
    '''
    
    # Beautify
    if args.output != 'cli':
        if len(content) > 1000000:
            content = content.replace(";",";\r\n").replace(",",",\r\n")
        else:
            content = jsbeautifier.beautify(content)
    
    items = re.findall(regex, content)
    items = list(set(items))
        
    # Match Regex
    filtered_items = []

    for item in items:
        # Remove other capture groups from regex results
        group = list(filter(None, item))

        if args.regex:
            if re.search(args.regex, group[1]):
                filtered_items.append(group)
        else:
            filtered_items.append(group)

    return filtered_items

def cli_output(endpoints):
    '''
    Output to CLI
    '''
    for endpoint in endpoints:
        print(cgi.escape(endpoint[1]).encode(
            'ascii', 'ignore').decode('utf8')) 

def html_save(html):
    '''
    Save as HTML file and open in the browser
    '''
    hide = os.dup(1)
    os.close(1)
    os.open(os.devnull, os.O_RDWR)
    try:
        s = Template(open('%s/template.html' % sys.path[0], 'r').read())

        text_file = open(args.output, "wb")
        text_file.write(s.substitute(content=html).encode('utf8'))
        text_file.close()

        print("URL to access output: file://%s" % os.path.abspath(args.output))
        file = "file:///%s" % os.path.abspath(args.output)
        if sys.platform == 'linux' or sys.platform == 'linux2':
            subprocess.call(["xdg-open", file])
        else:
            webbrowser.open(file)
    except Exception as e:
        print("Output can't be saved in %s \
            due to exception: %s" % (args.output, e))
    finally:
        os.dup2(hide, 1)

# Convert input to URLs or JS files
urls = parser_input(args.input)  

# Convert URLs to JS
html = ''
for url in urls:
    if not args.burp:
        try:
            file = send_request(url)
        except Exception as e:
            parser_error("invalid input defined or SSL error: %s" % e)
    else:
        file = url['js']
        url = url['url']

    endpoints = parser_file(file)
    if args.domain:
        for endpoint in endpoints:
            endpoint = cgi.escape(endpoint[1]).encode('ascii', 'ignore').decode('utf8')
            if endpoint[-3:] == ".js":
                if endpoint[:2] == "//":
                    endpoint = "https:" + endpoint
                print("Running against: " + endpoint)
                print("")
                try:
                    file = send_request(endpoint)
                    new_endpoints = parser_file(file)
                    if args.output == 'cli':
                        cli_output(new_endpoints)
                    else:
                        html += '''
                        <h1>File: <a href="%s" target="_blank" rel="nofollow noopener noreferrer">%s</a></h1>
                        ''' % (cgi.escape(url), cgi.escape(url))

                        for endpoint2 in new_endpoints:
                           url = cgi.escape(endpoint2[1])
                           string = "<div><a href='%s' class='text'>%s" % (
                              cgi.escape(url),
                              cgi.escape(url)
                           )
                           string2 = "</a><div class='container'>%s</div></div>" % cgi.escape(
                               endpoint2[0]
                           )
                           string2 = string2.replace(
                               cgi.escape(endpoint2[1]),
                               "<span style='background-color:yellow'>%s</span>" %
                               cgi.escape(endpoint2[1])
                           )
                           html += string + string2
                except Exception as e:
                    parser_error("invalid input defined or SSL error: %s" % e)
                print("")
    print("")
    print("Running against: " + args.input)
    print("")
    if args.output == 'cli':
        cli_output(endpoints)
    else:
        html += '''
            <h1>File: <a href="%s" target="_blank" rel="nofollow noopener noreferrer">%s</a></h1>
            ''' % (cgi.escape(url), cgi.escape(url))

        for endpoint in endpoints:
            url = cgi.escape(endpoint[1])
            string = "<div><a href='%s' class='text'>%s" % (
                cgi.escape(url),
                cgi.escape(url)
            )
            string2 = "</a><div class='container'>%s</div></div>" % cgi.escape(
                endpoint[0]
            )
            string2 = string2.replace(
                cgi.escape(endpoint[1]),
                "<span style='background-color:yellow'>%s</span>" %
                cgi.escape(endpoint[1])
            )

            html += string + string2

if args.output != 'cli':
    html_save(html)
