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

    def __init__(self, socket, message):
        super().__init__(socket)
        self.message = message

    def runCommand( self, command, action ):
        pass





