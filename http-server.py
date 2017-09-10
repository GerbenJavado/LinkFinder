import socket, re, urllib, os, colorama, platform, getpass, sys

colorama.init(autoreset=True)
if os.name != 'nt':
    if 'darwin' in platform.system().lower():
        os_path = '/Users'
    elif 'linux' in platform.system().lower():
        os_path = '/home'

    path_linkfinder = os.popen('''
                find %s/%s -type f -name "linkfinder.py" -exec grep -il "Gerben_Javado" {} \; -print -quit | awk '{print $1; exit}'
    ''' % (os_path, getpass.getuser())).read().replace('linkfinder.py','').rstrip()

else:
    path_linkfinder = ''
    if path_linkfinder = '':
        warning = """
                    It looks like you are using Windows and haven't changed the 'path_linkfinder' variable.\n
                    Please check the installation guide on Github or use this tool on Linux/OS X to fix this automatically.
                """
        print warning

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 8080)
s.bind(server_address)
s.listen(1)

while True:
  try:
    connection, client_address = s.accept()
    request = connection.recv(500)

    path = re.findall("GET /([^ ]*)", str(request))
    path = path[0] 
    file = str(path.split('?').pop(1).split('&')[0].split('=')[1])

    if (sys.version_info > (3, 0)):
        import urllib.parse
        url = urllib.parse.unquote(file)
    else:
        url = urllib.unquote(file).decode('utf8')

    print(colorama.Fore.RED + url)
    output = os.popen('python -u %s/linkfinder.py -o cli -i %s' % (path_linkfinder, "'" + url.replace("'", "'\\''") + "'")).read()
    if "SSL error" in output:
        output = os.popen('python -u %s/linkfinder.py -o cli -i %s' % (path_linkfinder, '"' + url.replace("'", "'\\''").replace("https", "http") + '"')).read()
        print("\n" + colorama.Fore.YELLOW + "SSL error, using http..\n")
    print(output)

    connection.close()
  except IndexError:
    pass
