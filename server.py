#  coding: utf-8 
import socketserver

# for HTTP Date header
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# Modifications from original version:
# Copyright 2023 Eric Brisson

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        # Workflow:
        # 1) receive request on web server self.request.recv()
        # 2) setup self.working_request with HTTPRequest object, which parses out method, protocol, headers, etc.
        # 3) call self.prepare_response()
        #    - return value of self.prepare_response() will be a Python string ready to respond
        #    - including all necessary headers
        #    - files requested, etc.
        #    - will logically prepare response depending on if it was possible (ie. don't have access, doesn't exist)
        # 4) return request from web server using self.request.sendall()
        # 5) print response (debug)

        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        self.handle_request()
        self.request.sendall(bytearray(self.working_response,'utf-8'))
        #self.print_response()
        
    def bad_request_resp(self):
        self.working_response = ""

        # add protocol, status code, and status name to response
        self.working_response += f"{self.protocol} 400 Bad Request\r\n"

        # prepare body
        body = "<!doctype html><html><body><h1>400 Bad Request</h1></body></html>"
        length = len(bytearray(body,'utf-8'))

        # add headers (?)
        now = datetime.now()
        stamp = mktime(now.timetuple())
        self.working_response += f"Date: {format_date_time(stamp)}\r\n" # Date -> Wed, 22 Oct 2008 10:52:40 GMT
        self.working_response += f"Content-Type: text/html\r\n" # Content-Type 
        self.working_response += f"Content-Length: {length}\r\n" # Content-Length
        self.working_response += f"\r\n" # Terminator

        self.working_response += f"{body}\r\n"

    def method_not_allowed_resp(self):
        self.working_response = ""

        # add protocol, status code, and status name to response
        self.working_response += f"{self.protocol} 405 Method Not Allowed\r\n"

        # prepare body
        body = "<!doctype html><html><body><h1>405 Method Not Allowed</h1></body></html>"
        length = len(bytearray(body,'utf-8'))

        # add headers (?)
        now = datetime.now()
        stamp = mktime(now.timetuple())
        self.working_response += f"Date: {format_date_time(stamp)}\r\n" # Date -> Wed, 22 Oct 2008 10:52:40 GMT
        self.working_response += f"Content-Type: text/html\r\n" # Content-Type 
        self.working_response += f"Content-Length: {length}\r\n" # Content-Length
        self.working_response += f"Allow: GET\r\n" # Need to indicate allowed methods
        self.working_response += f"\r\n" # Terminator

        self.working_response += f"{body}\r\n"

    def not_found_resp(self):
        self.working_response = ""

        # add protocol, status code, and status name to response
        self.working_response += f"{self.protocol} 404 Not Found\r\n"

        # prepare body
        body = "<!doctype html><html><body><h1>404 Not Found</h1></body></html>"
        length = len(bytearray(body,'utf-8'))

        # add headers (?)
        now = datetime.now()
        stamp = mktime(now.timetuple())
        self.working_response += f"Date: {format_date_time(stamp)}\r\n" # Date -> Wed, 22 Oct 2008 10:52:40 GMT
        self.working_response += f"Content-Type: text/html\r\n" # Content-Type 
        self.working_response += f"Content-Length: {length}\r\n" # Content-Length
        self.working_response += f"\r\n" # Terminator

        self.working_response += f"{body}\r\n"

    def moved_resp(self):
        self.working_response = ""

        # add protocol, status code, and status name to response
        self.working_response += f"{self.protocol} 301 Moved Permanently\r\n"

        # prepare body
        body = "<!doctype html><html><body><h1>301 Moved Permanently</h1></body></html>"
        length = len(bytearray(body,'utf-8'))

        # add headers (?)
        now = datetime.now()
        stamp = mktime(now.timetuple())
        self.working_response += f"Date: {format_date_time(stamp)}\r\n" # Date -> Wed, 22 Oct 2008 10:52:40 GMT
        self.working_response += f"Content-Type: text/html\r\n" # Content-Type 
        self.working_response += f"Content-Length: {length}\r\n" # Content-Length
        self.working_response += f"Location: http://{self.headers.get('host', '127.0.0.1')}:8080{self.path}/\r\n"
        self.working_response += f"\r\n" # Terminator

        self.working_response += f"{body}\r\n"

    def handle_request(self):
        # parse request
        self.working_request = self.parse_request()
        if not self.working_request:
            return

        if "Host" not in self.headers.keys():
            self.bad_request_resp()
            return False

        # self.print_request()
        # file retrieval logic
        file_path = "./www" + self.path
        if ".." in file_path:
            self.not_found_resp()
            return

        elif file_path[-1] == "/":
            file_path += "index.html"

        # init working response
        self.working_response = ""

        # open file
        try:
            file = open(file_path)

        except FileNotFoundError:
            self.not_found_resp()
            return

        except IsADirectoryError:
            self.moved_resp()
            return

        # prepare content-type
        content_type = ""
        if file_path[-5:] == ".html":
            content_type = "text/html"
        elif file_path[-4:] == ".css":
            content_type = "text/css"
        else:
            content_type="application/octet-stream"
        
        # add protocol, status code, and status name to response
        self.working_response += f"{self.protocol} 200 OK\r\n"

        # prepare body
        body = file.read()
        length = len(bytearray(body,'utf-8'))

        # add headers (?)
        now = datetime.now()
        stamp = mktime(now.timetuple())
        self.working_response += f"Date: {format_date_time(stamp)}\r\n" # Date -> Wed, 22 Oct 2008 10:52:40 GMT
        self.working_response += f"Content-Type: {content_type}\r\n" # Content-Type 
        self.working_response += f"Content-Length: {length}\r\n" # Content-Length
        self.working_response += f"\r\n" # Terminator

        self.working_response += f"{body}\r\n"
        return
    
    def print_request(self):
        print('-' * 80)
        print("REQUEST:")
        print("METHOD: " + self.method)
        print("PATH: " + self.path)
        print("PROTOCOL " + self.protocol)
        print("HEADERS:")
        for header in self.headers.keys():
            print(header + ": " + self.headers[header])
        print('-' * 80)
    
    def print_response(self):
        print("#" * 80)
        print("RESPONSE:")
        print(self.working_response)
        print("#" * 80)

    def parse_request(self):
        # take in the byte string of the request, decode it to string
        self.request_string = self.data.decode("utf-8")

        # set default protocol to HTTP/1.1
        self.protocol = "HTTP/1.1"

        # then attempt to parse it
        try:
            split_req = self.request_string.split("\r\n")

            # first element in split_req will contain method, path, and protocol
            self.method = split_req[0].split()[0]
            self.path = split_req[0].split()[1]
            self.protocol = split_req[0].split()[2]

            if self.method not in ['GET']:
                self.method_not_allowed_resp()
                return False

            # rest of split_req will contain headers
            headers = {}
            for each_header in split_req[1:]:
                header = each_header.split(":")[0].strip()
                value = each_header.split(":")[1].strip()
                headers[header] = value

            self.headers = headers

            return True

        except:
            self.bad_request_resp()
            return False

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
