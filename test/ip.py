import socks
import socket
import requests

socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)
socket.socket = socks.socksocket
print requests.get("http://icanhazip.com").text
