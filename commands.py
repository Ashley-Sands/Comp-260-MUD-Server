class CommandBase:
    def __init__(self, socket):
        self.socket = socket


class ClientNetworkCommand(CommandBase):

    def RunNetworkCommand( self, clients, send_message_func ):

        clientName = "Error"

        if self.socket in clients:
            clientName = clients[self.socket].clientName

        for sock in clients:
            if sock is not self.socket:
                send_message_func( sock, self.message( clientName ) )

    def message( self, clientName ):
        """
        :return: Message to send to other clients
        """
        pass


class ClientJoined(ClientNetworkCommand):
    def __init__(self, socket):
        super().__init__(socket)

    def message( self, clientName ):
        return clientName+" Has joint the server"


class ClientLost(ClientNetworkCommand):
    def __init__(self, socket):
        super().__init__(socket)

    def message( self, clientName ):
        return clientName+" Has become a zombie, watch out... (player left server)"


class ClientMessage(CommandBase):

    MESSAGE_TYPE_SELF       = 0     # send message to this socket only
    MESSAGE_TYPE_ALL        = 1     # send message to all clients including this client/socket
    MESSAGE_TYPE_ALL_OTHER  = 2     # send message to all clients excluding this client/socket
    MESSAGE_TYPE_ROOM       = 3     # send message to all clients with in the same room

    def __init__(self, socket, message, message_type):
        """
        :param socket:          This clients sockets
        :param message:         The message to be sent
        :param message_type:    Who to send the message to (MESSAGE_TYPE_SELF, MESSAGE_TYPE_ALL or MESSAGE_TYPE_ALL_OTHER)
        """
        super().__init__(socket)
        self.message = message
        self.message_type = message_type
        self.message_commands = { self.MESSAGE_TYPE_SELF:       self.message_self,
                                  self.MESSAGE_TYPE_ALL:        self.message_all,
                                  self.MESSAGE_TYPE_ALL_OTHER:  self.message_all_other,
                                  self.MESSAGE_TYPE_ROOM:       self.message_room
                                  }

    def senMessage( self, send_message_func, clients ):
        self.message_commands[self.message_type](send_message_func, clients)

    def message_self( self, send_message_func, clients ):
        if self.socket in clients:
            send_message_func(self.socket, self.message)

    def message_all( self, send_message_func, clients ):
        for c in clients:
            send_message_func(c, self.message)

    def message_all_other( self, send_message_func, clients ):

        for c in clients:
            if c is not self.socket:
                send_message_func(c, self.message)

    def message_room( self, send_message_func, clients ):

        client_room_id = ""

        if self.socket in clients:
            client_room_id = clients[self.socket].currentRoom

        for c in clients:
            if clients[c] is not self.socket and clients[c] == client_room_id:
                send_message_func( c, self.message )


class ClientAction( CommandBase ):

    def __init__(self, socket):
        super().__init__(socket)
        self.commands = { "help": self.help, "go": self.go, "talk": self.talk }

    def help( self, action ):
        """ Sends the use some help :)
        :param action:  Type of help to display, None to display all
        """
        pass

    def go( self, action ):
        """ Move the palyer into a valid room
        :param action:  direction to move in (north (or n), east (or e), south (or s), west (or w) )
        """
        pass

    def talk( self, action ):
        """Talk to the other users in the same room"""
        pass

    def shout( self, action ):
        """Shout a message, this will attract zombies for connected rooms and send the message to clients in connected rooms"""
        pass

    def attack( self, action ):
        """Attack a zombie or another player"""

    def search ( self, action ):
        """Searchers a dead player or zombie"""
        pass

    def error( self, command ):

        return "Error: Command "+ str(command) +" not found."




