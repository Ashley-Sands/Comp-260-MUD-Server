from Commands.message import *

class ClientActionDispatcher( ClientCommand ):

    def __init__(self, socket, message):
        super().__init__(socket)
        self.commands = { "help": ClientActionHelp, "go": ClientActionGo, "talk": ClientActionTalk, "room": ClientActionRoom }
        self.message = message

    def RunCommand( self, clients, dungeon ):

        followUpCommands = []

        user_input = self.message.split( ' ' )
        command = user_input[0].lower()
        action = ""

        if command != "help" and len(user_input) < 2 or command not in self.commands:
            return [ ClientMessage( self.socket, "Invalid command", ClientMessage.MESSAGE_TYPE_SELF ) ]

        if len(user_input) >= 2:
            action = ' '.join(user_input[1:])

        return self.commands[ command ](self.socket, action).RunCommand( clients, dungeon )


class ClientActionHelp( ClientAction ):

    def __init__(self, socket, action):
        super().__init__(socket, action)

        self.help_func = { "room" : self.help_room,
                           "health": self.help_health }

    def RunCommand( self, clients, dungeon ):

        if self.socket not in clients:
            return []

        if self.action.lower() in self.help_func:
            help = self.help_func[self.action.lower()](clients)
        else:
            help = dungeon.DisplayRoomOptions( clients[self.socket].currentRoom )

        #help = "\nType 'go [direction]' to move into another room\n"
        #help = help + "[Directions]\n"
        #help = help + "North\nEast\nSouth\nWest"

        return [ClientMessage(self.socket, help, ClientMessage.MESSAGE_TYPE_SELF)]

    def help_room( self, clients ):
        return "While stareing blankly throught the dark gloomy room you notice that\n" \
               "someone has writen '"+clients[self.socket].currentRoom.upper()+"' in blood on the wall"

    def help_health( self, clients ):
        return "Remaining Health: "+ str(clients[self.socket].health)


class ClientActionGo(ClientAction):

    def RunCommand( self, clients, dungeon ):
        if self.socket not in clients:
            return [ ]

        valid, roomName = dungeon.MovePlayer(self.action, clients[ self.socket ].currentRoom )
        clientName = clients[self.socket].clientName

        if valid:
            clients[ self.socket ].currentRoom = roomName
            return ClientActionHelp(self.socket, self.action).RunCommand(clients, dungeon) + \
                   [ClientMessage(self.socket, "Has enter the room!", ClientMessage.MESSAGE_TYPE_ROOM)]
        else:
            clients[ self.socket ].health -= 1
            return [ClientMessage(self.socket, "You walk straight into a brick wall (-1 hp)\n**Ouch**\n", ClientMessage.MESSAGE_TYPE_SELF)] + \
                ClientActionHelp(self.socket, "health").RunCommand(clients, dungeon)



class ClientActionTalk(ClientAction):

    def RunCommand( self, clients, dungeon ):
        return [ ClientMessage( self.socket, self.action, ClientMessage.MESSAGE_TYPE_ROOM ) ]

class ClientActionRoom(ClientAction):

    def RunCommand( self, clients, dungeon ):
        return [ ClientMessage( self.socket, self.action, ClientMessage.MESSAGE_TYPE_ROOM ) ]