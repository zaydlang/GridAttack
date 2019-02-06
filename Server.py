import socketserver

games = []

class Game():
    def __init__(self, host_player):
        self.host_player = host_player
        self.join_player = None
        self.status = "joinable"
        games.append(self)

    def set_opponent(self, opponent):
        self.join_player = opponent

class Player(socketserver.BaseRequestHandler): 
    def handle(self):
        args = self.request.recv(1024).strip().decode().split(" ")
        
        if args[0] == "verify":
            if len(args) > 1:
                self.name = args[1]
                self.send_message("accept")
                self.verified = True
                self.in_game = False
            else:
                self.verified = False
                self.send_message("decline")

        if self.verified == True:      
            if args[0] == "list":
                self.request.send(';'.join(game.host_player.name for game in games))
            elif args[0] == "create":
                if self.in_game == False:   
                    self.in_game = True
                    self.game = Game(self)
            elif args[0] == "join":
                game = next((game for game in games if game.host_player.name == button_pressed), None)
                if game is not None:
                    self.send_message("accept")
                    game.set_opponent(self)
                else:
                    self.send_message("decline")

    def send_message(self, message):
        print(message)
        self.request.send(message.encode())
        
host, port = "0.0.0.0", 34197
server = socketserver.TCPServer((host, port), Player)
print("Server started on port " + str(port))
server.serve_forever()
