from Commands.message import *

class ClientActionDispatcher( ClientCommand ):

    def __init__(self, socket, message):
        super().__init__(socket)
        self.commands = { "help": ClientActionHelp, "go": ClientActionGo, "talk": ClientActionTalk }
        self.message = message

    def RunCommand( self, clients, dungeon ):

        followUpCommands = []

        user_input = self.message.split( ' ' )
        command = user_input[0].lower()
        action = ""

        if command != "help" and len(user_input) < 2 or command not in self.commands:
            return [ ClientMessage( self.socket, "Invalid command", ClientMessage.MESSAGE_TYPE_SELF ) ]

        if len(user_input) >= 2:
            action = user_input[1].lower()

        return self.commands[ command ](self.socket, action).RunCommand( clients, dungeon )


class ClientActionHelp( ClientAction ):

    def RunCommand( self, clients, dungeon ):

        help = dungeon.DisplayCurrentRoom()
        #help = "\nType 'go [direction]' to move into another room\n"
        #help = help + "[Directions]\n"
        #help = help + "North\nEast\nSouth\nWest"

        return [ClientMessage(self.socket, help, ClientMessage.MESSAGE_TYPE_SELF)]


class ClientActionGo(ClientAction):

    def RunCommand( self, clients, dungeon ):
        message = dungeon.MovePlayer(self.action)
        return [ ClientMessage( self.socket, message, ClientMessage.MESSAGE_TYPE_SELF ) ]


class ClientActionTalk(ClientAction):

    def RunCommand( self, clients, dungeon ):
        return [ ClientMessage( self.socket, self.action, ClientMessage.MESSAGE_TYPE_ALL_OTHER ) ]
