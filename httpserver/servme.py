import http.server
import socketserver
import socket
import subprocess
import os

hotspot=input('Enter your hotspotname:')
password=input('Enter your password:')
os.system('netsh wlan set hostednetwork mode=allow ssid='+hotspot+' key='+password)
os.system('netsh wlan start hostednetwork')
ipadrs=str(socket.gethostbyname(socket.gethostname()))
PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

print('Open http://'+ipadrs+':'+str(PORT)+' in browser')
print('To stop press Ctrl+c')
try:
	httpd.serve_forever()
except KeyboardInterrupt:
	os.system('netsh wlan stop hostednetwork')