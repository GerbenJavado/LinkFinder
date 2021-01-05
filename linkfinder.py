#!/usr/bin/env python
# Python 3
# LinkFinder
# By Gerben_Javado

# Fix webbrowser bug for MacOS
import os
os.environ["BROWSER"] = "open"

# Import libraries
import re, sys, glob, html, argparse, jsbeautifier, webbrowser, subprocess, base64, ssl, xml.etree.ElementTree

from gzip import GzipFile
from string import Template

try:
    from StringIO import StringIO
    readBytesCustom = StringIO
except ImportError:
    from io import BytesIO
    readBytesCustom = BytesIO

try:
    from urllib.request import Request, urlopen
except ImportError:
    from urllib2 import Request, urlopen

# Regex used
regex_str = r"""

  (?:"|')                               # Start newline delimiter

  (
    ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
    [^"'/]{1,}\.                        # Match a domainname (any character + dot)
    [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path

    |

    ((?:/|\.\./|\./)                    # Start with /,../,./
    [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
    [^"'><,;|()]{1,})                   # Rest of the characters can't be

    |

    ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
    [a-zA-Z0-9_\-/]{1,}                 # Resource name
    \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters

    |

    ([a-zA-Z0-9_\-/]{1,}/               # REST API (no extension) with /
    [a-zA-Z0-9_\-/]{3,}                 # Proper REST endpoints usually have 3+ chars
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters

    |

    ([a-zA-Z0-9_\-]{1,}                 # filename
    \.(?:php|asp|aspx|jsp|json|
         action|html|js|txt|xml)        # . + extension
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters

  )

  (?:"|')                               # End newline delimiter

"""

context_delimiter_str = "\n"

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

    q.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
    q.add_header('Accept', 'text/html,\
        application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    q.add_header('Accept-Language', 'en-US,en;q=0.8')
    q.add_header('Accept-Encoding', 'gzip')
    q.add_header('Cookie', args.cookies)

    try:
        sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        response = urlopen(q, timeout=args.timeout, context=sslcontext)
    except:
        sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        response = urlopen(q, timeout=args.timeout, context=sslcontext)

    if response.info().get('Content-Encoding') == 'gzip':
        data = GzipFile(fileobj=readBytesCustom(response.read())).read()
    elif response.info().get('Content-Encoding') == 'deflate':
        data = response.read().read()
    else:
        data = response.read()

    return data.decode('utf-8', 'replace')

def getContext(list_matches, content, include_delimiter=0, context_delimiter_str="\n"):
    '''
    Parse Input
    list_matches:       list of tuple (link, start_index, end_index)
    content:            content to search for the context
    include_delimiter   Set 1 to include delimiter in context
    '''
    items = []
    for m in list_matches:
        match_str = m[0]
        match_start = m[1]
        match_end = m[2]
        context_start_index = match_start
        context_end_index = match_end
        delimiter_len = len(context_delimiter_str)
        content_max_index = len(content) - 1

        while content[context_start_index] != context_delimiter_str and context_start_index > 0:
            context_start_index = context_start_index - 1

        while content[context_end_index] != context_delimiter_str and context_end_index < content_max_index:
            context_end_index = context_end_index + 1

        if include_delimiter:
            context = content[context_start_index: context_end_index]
        else:
            context = content[context_start_index + delimiter_len: context_end_index]

        item = {
            "link": match_str,
            "context": context
        }
        items.append(item)

    return items

def parser_file(content, regex_str, mode=1, more_regex=None, no_dup=1):
    '''
    Parse Input
    content:    string of content to be searched
    regex_str:  string of regex (The link should be in the group(1))
    mode:       mode of parsing. Set 1 to include surrounding contexts in the result
    more_regex: string of regex to filter the result
    no_dup:     remove duplicated link (context is NOT counted)

    Return the list of ["link": link, "context": context]
    The context is optional if mode=1 is provided.
    '''
    global context_delimiter_str

    if mode == 1:
        # Beautify
        if len(content) > 1000000:
            content = content.replace(";",";\r\n").replace(",",",\r\n")
        else:
            content = jsbeautifier.beautify(content)

    regex = re.compile(regex_str, re.VERBOSE)

    if mode == 1:
        all_matches = [(m.group(1), m.start(0), m.end(0)) for m in re.finditer(regex, content)]
        items = getContext(all_matches, content, context_delimiter_str=context_delimiter_str)
    else:
        items = [{"link": m.group(1)} for m in re.finditer(regex, content)]

    if no_dup:
        # Remove duplication
        all_links = set()
        no_dup_items = []
        for item in items:
            if item["link"] not in all_links:
                all_links.add(item["link"])
                no_dup_items.append(item)
        items = no_dup_items

    # Match Regex
    filtered_items = []
    for item in items:
        # Remove other capture groups from regex results
        if more_regex:
            if re.search(more_regex, item["link"]):
                filtered_items.append(item)
        else:
            filtered_items.append(item)

    return filtered_items

def cli_output(endpoints):
    '''
    Output to CLI
    '''
    for endpoint in endpoints:
        print(html.escape(endpoint["link"]).encode(
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

def check_url(url):
    nopelist = ["node_modules", "jquery.js"]
    if url[-3:] == ".js":
        words = url.split("/")
        for word in words:
            if word in nopelist:
                return False
        if url[:2] == "//":
            url = "https:" + url
        if url[:4] != "http":
            if url[:1] == "/":
                url = args.input + url
            else:
                url = args.input + "/" + url
        return url
    else:
        return False

if __name__ == "__main__":
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
    default_timeout = 10
    parser.add_argument("-t", "--timeout",
                        help="How many seconds to wait for the server to send data before giving up (default: " + str(default_timeout) + " seconds)",
                        default=default_timeout, type=int, metavar="<seconds>")
    args = parser.parse_args()

    if args.input[-1:] == "/":
        args.input = args.input[:-1]

    mode = 1
    if args.output == "cli":
        mode = 0

    # Convert input to URLs or JS files
    urls = parser_input(args.input)

    # Convert URLs to JS
    output = ''
    for url in urls:
        if not args.burp:
            try:
                file = send_request(url)
            except Exception as e:
                parser_error("invalid input defined or SSL error: %s" % e)
        else:
            file = url['js']
            url = url['url']

        endpoints = parser_file(file, regex_str, mode, args.regex)
        if args.domain:
            for endpoint in endpoints:
                endpoint = html.escape(endpoint["link"]).encode('ascii', 'ignore').decode('utf8')
                endpoint = check_url(endpoint)
                if endpoint is False:
                    continue
                print("Running against: " + endpoint)
                print("")
                try:
                    file = send_request(endpoint)
                    new_endpoints = parser_file(file, regex_str, mode, args.regex)
                    if args.output == 'cli':
                        cli_output(new_endpoints)
                    else:
                        output += '''
                        <h1>File: <a href="%s" target="_blank" rel="nofollow noopener noreferrer">%s</a></h1>
                        ''' % (html.escape(endpoint), html.escape(endpoint))

                        for endpoint2 in new_endpoints:
                            url = html.escape(endpoint2["link"])
                            header = "<div><a href='%s' class='text'>%s" % (
                                html.escape(url),
                                html.escape(url)
                            )
                            body = "</a><div class='container'>%s</div></div>" % html.escape(
                                endpoint2["context"]
                            )
                            body = body.replace(
                                html.escape(endpoint2["link"]),
                                "<span style='background-color:yellow'>%s</span>" %
                                html.escape(endpoint2["link"])
                            )
                            output += header + body
                except Exception as e:
                    print("Invalid input defined or SSL error for: " + endpoint)
                    continue

        if args.output == 'cli':
            cli_output(endpoints)
        else:
            output += '''
                <h1>File: <a href="%s" target="_blank" rel="nofollow noopener noreferrer">%s</a></h1>
                ''' % (html.escape(url), html.escape(url))

            for endpoint in endpoints:
                url = html.escape(endpoint["link"])
                header = "<div><a href='%s' class='text'>%s" % (
                    html.escape(url),
                    html.escape(url)
                )
                body = "</a><div class='container'>%s</div></div>" % html.escape(
                    endpoint["context"]
                )
                body = body.replace(
                    html.escape(endpoint["link"]),
                    "<span style='background-color:yellow'>%s</span>" %
                    html.escape(endpoint["link"])
                )

                output += header + body

    if args.output != 'cli':
        html_save(output)
