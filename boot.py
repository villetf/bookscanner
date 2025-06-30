import config.keys as keys
import network
from time import sleep
from buzzer import soundBuzzer
from ledLight import powerOnLed

def connect():
   powerOnLed('yellow')
   wlan = network.WLAN(network.STA_IF)         # Put modem on Station mode
   if not wlan.isconnected():                  # Check if already connected
      print('connecting to network...s')
      wlan.active(True)                       # Activate network interface
      # set power mode to get WiFi power-saving off (if needed)
      wlan.config(pm = 0xa11140)
      wlan.connect(keys.WIFI_SSID, keys.WIFI_PASS)  # Your WiFi Credential
      print('Waiting for connection...', end='')
      # Check if it is connected otherwise wait
      while not wlan.isconnected() and wlan.status() >= 0:
         print('.', end='')
         sleep(1)
   # Print the IP assigned by router
   ip = wlan.ifconfig()[0]
   print('\nConnected on {}'.format(ip))
   return ip

def http_get(url = 'http://detectportal.firefox.com/'):
   import socket                           # Used by HTML get request
   import time                             # Used for delay
   _, _, host, path = url.split('/', 3)    # Separate URL request
   addr = socket.getaddrinfo(host, 80)[0][-1]  # Get IP address of host
   s = socket.socket()                     # Initialise the socket
   s.connect(addr)                         # Try connecting to host address
   # Send HTTP request to the host with specific path
   s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))    
   time.sleep(1)                           # Sleep for a second
   rec_bytes = s.recv(10000)               # Receve response
   print(rec_bytes)                        # Print the response
   s.close()                               # Close connection
   soundBuzzer(0.1)
   soundBuzzer(0.1)
   soundBuzzer(0.1)

# WiFi Connection
try:
   ip = connect()
except KeyboardInterrupt:
   print("Keyboard interrupt")

# HTTP request
try:
   http_get()
except (Exception, KeyboardInterrupt) as err:
   print("No Internet", err)
