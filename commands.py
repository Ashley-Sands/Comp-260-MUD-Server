class CommandBase:
    def __init__(self, socket):
        self.socket = socket

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

        clientExist = self.socket in clients

        for c in clients:
            if not clientExist or ( clientExist and c is not self.socket ):
                send_message_func(c, self.message)

    def message_room( self, send_message_func, clients ):

        client_room_id = ""

        if self.socket in clients:
            client_room_id = clients[self.socket].currentRoom

        for c in clients:
            if clients[c] is not self.socket and clients[c] == client_room_id:
                send_message_func( c, self.message )


class ClientCommand(CommandBase):

    def RunCommand( self, clients ):
        """ Runs the command returning a list of follow up commands

        :param clients:     list of current active clients
        :return:            a list of follow up commands.
        """
        pass


class ClientNetworkCommand(ClientCommand):

    def RunCommand( self, clients ):

        clientName = "Error"

        if self.socket in clients:
            clientName = clients[self.socket].clientName

        return [ ClientMessage(self.socket, self.message( clientName ), ClientMessage.MESSAGE_TYPE_ALL_OTHER ) ]

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


class ClientActionDispatcher( ClientCommand ):

    def __init__(self, socket, message):
        super().__init__(socket)
        self.commands = { "help": ClientActionHelp, "go": self.go, "talk": self.talk }
        self.message = message

    def RunCommand( self, clients ):

        followUpCommands = []

        user_input = self.message.split(' ')

        if type(user_input) is not list or len(user_input) < 2 or user_input[0] not in self.commands:
            return [ ClientMessage( self.socket, "Invalid command", ClientMessage.MESSAGE_TYPE_SELF ) ]

        return self.commands[ user_input ](self.socket, user_input[1]).runAction( clients )

class ClientAction(ClientCommand):

    def __init__(self, socket, action):
        super().__init__(socket)
        self.action = action

class ClientActionHelp( ClientAction ):

    def RunCommand( self, clients ):

        help = "Type 'go [direction]' to move into another room\n"
        help = help + " [Directions] \n"
        help = help + " North\nEast\nSouth\nWest"

        return [ClientMessage(self.socket, help, ClientMessage.MESSAGE_TYPE_SELF)]

class ClientActionGo():
    pass