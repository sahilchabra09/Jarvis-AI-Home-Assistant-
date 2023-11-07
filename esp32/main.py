import machine
import usocket as socket
import time
import network

# Initialize a timeout variable for WiFi connection
timeout = 0

# Create a network.WLAN object to manage the WiFi connection
wifi = network.WLAN(network.STA_IF)

# Restart WiFi by disabling and re-enabling it
wifi.active(False)
time.sleep(0.5)
wifi.active(True)

# Connect to a WiFi network with SSID 'Arc' and password 'qwerty0902'
wifi.connect('Jarvis', '12345678')

if not wifi.isconnected():
    print('Connecting...')
    while (not wifi.isconnected() and timeout < 5):
        print(5 - timeout)
        timeout = timeout + 1
        time.sleep(1)

if wifi.isconnected():
    print('Connected to the network')
    print('Network configuration:', wifi.ifconfig())

# HTML Document
html = '''<!DOCTYPE html>
<html>
<center><h2>ESP32 Relay Control</h2></center>
<form>
<center>
<h3>Relay 1 Control</h3>
<button name="Relay1" value='ON' type='submit'>Turn ON</button>
<button name="Relay1" value='OFF' type='submit'>Turn OFF</button>
<h3>Relay 2 Control</h3>
<button name="Relay2" value='ON' type='submit'>Turn ON</button>
<button name="Relay2" value='OFF' type='submit'>Turn OFF</button>
</center>
'''

# Relay Pin Declarations (GPIO Pin 12 for Relay 1 and GPIO Pin 13 for Relay 2)
RELAY_PIN_1 = machine.Pin(4, machine.Pin.OUT)
RELAY_PIN_2 = machine.Pin(5, machine.Pin.OUT)

# Initialize the relays to the OFF state (1 - inverted logic)
RELAY_PIN_1.value(1)
RELAY_PIN_2.value(1)

# Initializing a socket for the web server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET - Internet Socket, SOCK_STREAM - TCP protocol

Host = ''  # An empty string allows connections from all IP addresses
Port = 80  # Port 80 is used for HTTP
s.bind((Host, Port))  # Bind the socket to the host and port

s.listen(5)  # Listen for up to 5 clients simultaneously

# Main loop
while True:
    connection_socket, address = s.accept()  # Accept a new connection and get the socket and address of the client
    print('Got a connection from', address)
    request = connection_socket.recv(1024)  # Receive the client's request, up to 1024 bytes
    print('Content', request)  # Print the received request
    request = str(request)  # Convert the request from bytes to a string

    # Check if the request contains '/?Relay1=ON' or '/?Relay1=OFF' indicating a relay 1 control request
    RELAY1_ON = request.find('/?Relay1=ON')
    RELAY1_OFF = request.find('/?Relay1=OFF')

    # Check if the request contains '/?Relay2=ON' or '/?Relay2=OFF' indicating a relay 2 control request
    RELAY2_ON = request.find('/?Relay2=ON')
    RELAY2_OFF = request.find('/?Relay2=OFF')

    # If '/?Relay1=ON' is found in the request, turn Relay 1 ON (set GPIO pin to 0 - inverted logic)
    if RELAY1_ON >= 0:
        RELAY_PIN_1.value(0)

    # If '/?Relay1=OFF' is found in the request, turn Relay 1 OFF (set GPIO pin to 1 - inverted logic)
    if RELAY1_OFF >= 0:
        RELAY_PIN_1.value(1)

    # If '/?Relay2=ON' is found in the request, turn Relay 2 ON (set GPIO pin to 0 - inverted logic)
    if RELAY2_ON >= 0:
        RELAY_PIN_2.value(0)

    # If '/?Relay2=OFF' is found in the request, turn Relay 2 OFF (set GPIO pin to 1 - inverted logic)
    if RELAY2_OFF >= 0:
        RELAY_PIN_2.value(1)
        
    try:
        # Send the HTML document as a response to the connected client
        response = html
        connection_socket.send(response)
    except OSError as e:
        print('Error sending response:', e)

    # Close the connection socket for this client
    connection_socket.close()
