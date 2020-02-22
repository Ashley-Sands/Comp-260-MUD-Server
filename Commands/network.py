from Commands.message import *
from Commands.actions import ClientActionHelp

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

    def welcome( self ):

        welcome_msg = "For the past 3 days you have been hunted by rough gang of bandits,\n" \
                      "you've had no sleep, no food and only drank from dirty puddles.\n" \
                      "You find an abandoned building and hide in empty cupboard ....\n..\n..\n..\n" \
                      "**BANG**\n" \
                      "You awaken, startled. As you come around you realize that closet door open\n" \
                      "You know you shut it. As you gaze out into room to notice the door you enter\n" \
                      "through is now closed. You slower climb of the cupboard and wonder over to the door\n" \
                      "\n\n It's Locked...\n" \
                      "You hear some rustling come from your left and suddenly realize you're not alone\n" \
                      "There's are guy slumped up againes the wall covered in blood and with his last breaths\n" \
                      "says 'go north.........' as you watch him past away.\n"

        return [ClientMessage(self.socket, welcome_msg, ClientMessage.MESSAGE_TYPE_SELF, False)]


class ClientLost(ClientNetworkCommand):
    def __init__(self, socket):
        super().__init__(socket)

    def message( self, clientName ):
        return clientName+" Has become a zombie, watch out... (player left server)"
