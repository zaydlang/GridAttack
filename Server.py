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
                self.request.send("accept".encode())
                self.verified = True
                self.in_game = False
            else:
                self.verified = False
                self.request.send("decline".encode())

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
                    self.request.send("accept".encode())
                    game.set_opponent(self)
                else:
                    self.request.send("decline".encode())
        else:
            close()
        
host, port = "0.0.0.0", 34197
server = socketserver.TCPServer((host, port), Player)
server.serve_forever()
