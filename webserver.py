# Author: Chris McDonald
# Web Server implemented using Python
# Only handles GET commands

#!/usr/bin/env python

import socket

# Class object which stores the value of each header and the content of the file
class Header:
    def __init__(self, code, location, connection, contentType, content):
        self.code = code # Status Code
        self.location = location # Location header
        self.connection = connection # Connection header
        self.contentType = contentType # Content-Type header
        self.content = content # The content of the file being opened

    # Converts the data stored in the Header object into one string concatenation
    def toStringRedirect(self): # This string contains the location header needed for redirects
        headerString = ('HTTP/1.1 %s \nLocation: %s \nConnection: %s \nContent-Type: %s \nContent-Length: %s \n%s \n' % (str(self.code), str(self.location), str(self.connection), str(self.contentType), str(len(self.content)), str(self.content)))
        return headerString
    def toString(self):
        headerString = ('HTTP/1.1 %s \nConnection: %s \nContent-Type: %s \nContent-Length: %s \n%s \n' % (str(self.code), str(self.connection), str(self.contentType), str(len(self.content)), str(self.content)))
        return headerString

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('',7000)) # Opens the socket to ('Server Location', Port #)
    sock.listen(5)

    # Initialized Header objects with the 3 status codes used within the scope of this project
    # The default Content-Type attribute is text/plain in order to retain the format of the file
    header_200 = Header('200', ' ', 'close', 'text/plain', ' ') # Status Code: 200 - Ok
    header_302 = Header('302', ' ', 'close', 'text/plain', ' ') # Status Code: 302 - Redirect
    header_404 = Header('404', ' ', 'close', 'text/plain', ' ') # Status Code: 404 - Page Not Found
    # The sendHeader variable holds the string value of the Header object

    # Root of the Web Server being used - location of all files
    doc_root = '/home/cjmcdona'
    # Equivalent to Index.html - if no file path is defined, then default to this location
    doc_index = '/default.html'
    # Location of the 404 page
    doc_error404 = '/error404.html'
    # Dictionary to store {key: value} pairs for redirection URLs
    redirectURL = {'/google' : 'http://www.google.com',
                   '/bu' : 'http://www.butler.edu'}
    # Temporarily stores the Content-Type of the file
    tempContentType = ''
    # Main loop to handle connections to the server
    while True:
        conn, client_address = sock.accept()
        data = conn.recv(1024)
        # Reset the Content-Type to the default for reading files
        tempContentType = 'text/plain'
        print('Client connected...')
        print('Received:\n%s' % (data)) # Display information on the server
        line_0 = data.split('\n')
        filePath = line_0[0].split(' ')[1] # Extracts the file path found after the GET command
        if(filePath == '/' or filePath == '/favicon.ico'):
                filePath = doc_index
        if '.' in filePath:
            findExtension = filePath.split('.')[1] # Extracts the extension of the file from the file path
            if findExtension == 'txt':
                tempContentType = 'text/plain'
            if findExtension == 'html':
                tempContentType = 'text/html'
            if findExtension == 'jpg' or findExtension == '.jpeg':
                tempContentType = 'image/jpeg'
            if findExtension == 'png':
                tempContentType = 'image/png'
            if findExtension == 'gif':
                tempContentType = 'image/gif'
            if findExtension == 'css':
                tempContentType = 'text/css'
            if findExtension == 'js':
                tempContentType = 'application/javascript'
            header_200.contentType = tempContentType
        #sendHeader = header_200.toString()
        # Try to open the file
        try:
            with open(doc_root + filePath, 'rb') as file:
                header_200.content = file.read()
            sendHeader = header_200.toString()
        # Handles the case where the file path is not a file on the server
        except IOError:
            # Quick solution to handle redirection
            if filePath == '/google' or filePath == '/bu':
                for key in redirectURL:
                    if filePath == key:
                        header_302.location = redirectURL[key]
                        sendHeader = header_302.toStringRedirect()
            # Displays the 404 page
            else:
                header_404.contentType = 'text/html'
                with open(doc_root + doc_error404, 'r') as file:
                    header_404.content = file.read()
                sendHeader = header_404.toString()
        print(sendHeader)
        conn.send(sendHeader)
        conn.close()

if __name__ == '__main__':
    main()
