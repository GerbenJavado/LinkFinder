import socket, re, urllib, os, colorama, sys

colorama.init(autoreset=True)
path_linkfinder = '/Applications/Pentesting/LinkFinder'

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
    print(output)

    connection.close()
  except IndexError:
    pass