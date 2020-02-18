from Commands.Message import *

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
