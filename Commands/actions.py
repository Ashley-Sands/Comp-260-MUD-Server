from Commands.Message import *

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



class ClientActionHelp( ClientAction ):

    def RunCommand( self, clients ):

        help = "Type 'go [direction]' to move into another room\n"
        help = help + " [Directions] \n"
        help = help + " North\nEast\nSouth\nWest"

        return [ClientMessage(self.socket, help, ClientMessage.MESSAGE_TYPE_SELF)]

class ClientActionGo():
    pass