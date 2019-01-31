import socketserver

class ConnectionHandler(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data.decode())
        
host, port = "0.0.0.0", 34197
server = socketserver.TCPServer((host, port), ConnectionHandler)
server.serve_forever()
