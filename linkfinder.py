#!/usr/bin/env python
# Python 2.7.x - 3.6.x
# LinkFinder
# By Gerben_Javado

# Fix webbrowser bug for MacOS
import os
os.environ["BROWSER"] = "open"

# Import libraries
import re, sys, glob, cgi, argparse, requests, urllib, jsbeautifier, webbrowser, subprocess, base64, xml.etree.ElementTree

from requests_file import FileAdapter
from string import Template
from requests.packages.urllib3.exceptions import InsecureRequestWarning 

# Regex used
regex = re.compile(r"""

  ([^\n]*(?:"|')                    # Start newline delimiter

  (?:
    ((?:[a-zA-Z]{1,10}://|//)       # Match a scheme [a-Z]*1-10 or //
    [^"'/]{1,}\.                    # Match a domainname (any character + dot)
    [a-zA-Z]{2,}[^"']{0,})          # The domainextension and/or path

    |

    ((?:/|\.\./|\./)                # Start with /,../,./
    [^"'><,;| *()(%$^/\\\[\]]       # Next character can't be... 
    [^"'><,;|()]{1,})               # Rest of the characters can't be

    |

    ([a-zA-Z0-9/]{1,}/              # Relative endpoint with /
    [a-zA-Z0-9_\-/]{1,}\.[a-z]{1,4} # Rest + extension
    (?:[\?|/][^"|']{0,}|))          # ? mark with parameters

    |

    ([a-zA-Z0-9_\-]{1,}             # filename
    \.(?:php|asp|aspx|jsp)          # . + extension
    (?:\?[^"|']{0,}|))              # ? mark with parameters
 
  )             
  
  (?:"|')[^\n]*)                    # End newline delimiter

""", re.VERBOSE)

# Parse command line
parser = argparse.ArgumentParser()
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
            jsfiles.append(base64.b64decode(item.find('response').text).decode('utf-8'))
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
        be found.")]


def send_request(url):
    '''
    Send requests with Requests
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept': 'text/html,\
        application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8',
        'Accept-Encoding': 'gzip',
        'Cookie': args.cookies
    }

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    s = requests.Session()
    s.mount('file://', FileAdapter())
    content = s.get(url, headers=headers, timeout=1, stream=True, verify=False)
    return content.text if hasattr(content, "text") else content.content


def parser_file(content):
    '''
    Parse Input
    '''
    
    # Beautify
    content = jsbeautifier.beautify(content)
    items = re.findall(regex, content)
        
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
        file = "file://%s" % os.path.abspath(args.output)
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
for url in urls:
    if not args.burp:
        try:
            file = send_request(url)
        except Exception as e:
            parser_error("invalid input defined or SSL error: %s" % e)
    else: 
        file = url

    endpoints = parser_file(file)
    html = ''

    if args.output == 'cli':
        cli_output(endpoints)
    else:

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
