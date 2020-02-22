from Commands.message import *


class ClientActionHelp( ClientAction ):

    def __init__(self, socket, action):
        super().__init__(socket, action)

        self.help_func = { "location" : self.help_room,
                           "health": self.help_health,
                           "options": self.help_options
                           }

    def RunCommand( self, clients, dungeon ):

        if self.socket not in clients:
            return []

        if self.action.lower() in ClientActionDispatcher.commands:
            help = ClientActionDispatcher.commands[self.action.lower()].ActionHelp( ClientActionDispatcher.commands[self.action.lower()], self.action.lower() )
        elif self.action.lower() in self.help_func:
            help = self.help_func[self.action.lower()](clients, dungeon)
        else:
            help = self.default_help()

        return [ClientMessage(self.socket, help, ClientMessage.MESSAGE_TYPE_SELF, False)]

    def default_help( self ):

        return "HHHHHHHHHHHHHEEEEEEEEEEEEEEELLLLLLLLLLLLLLPPPPPPPPPPPP!\n**No one can here you screams**"

    def help_room( self, clients, dungeon ):
        return "While stareing blankly throught the dark gloomy room you notice that\n" \
               "someone has writen '"+clients[self.socket].currentRoom.upper()+"' in blood on the wall"

    def help_health( self, clients, dungeon ):
        return "Remaining Health: "+ str(clients[self.socket].health)

    def help_options( self, clients, dungeon ):
        return dungeon.DisplayRoomOptions( clients[self.socket].currentRoom )


class ClientActionGo(ClientAction):

    def RunCommand( self, clients, dungeon ):
        if self.socket not in clients:
            return [ ]

        # move the client in the direction thy want to move
        valid, roomName = dungeon.MovePlayer(self.action, clients[ self.socket ].currentRoom )
        clientName = clients[self.socket].clientName

        # if the move is vaild move them into the room else
        # walk into a brick wall causing one damage
        if valid:
            clients[ self.socket ].currentRoom = roomName
            return ClientActionHelp(self.socket, "options").RunCommand(clients, dungeon) + \
                   [ClientMessage(self.socket, "Has enter the room!", ClientMessage.MESSAGE_TYPE_ROOM)]
        else:
            clients[ self.socket ].health -= 1
            return [ClientMessage(self.socket, "You walk straight into a brick wall (-1 hp)\n**Ouch**\n", ClientMessage.MESSAGE_TYPE_SELF)] + \
                ClientActionHelp(self.socket, "health").RunCommand(clients, dungeon)



class ClientActionTalk(ClientAction):

    def RunCommand( self, clients, dungeon ):
        return [ ClientMessage( self.socket, self.action, ClientMessage.MESSAGE_TYPE_ROOM ) ]

    def ActionHelp(self, name):
        return ""

class ClientActionRoom(ClientAction):

    def RunCommand( self, clients, dungeon ):
        return [ ClientMessage( self.socket, self.action, ClientMessage.MESSAGE_TYPE_ROOM ) ]

class ClientActionRename(ClientAction):

    def RunCommand( self, clients, dungeon ):

        # check that the name is not already taken
        for c in clients:
            if self.action == clients[c].clientName:
                return [ClientMessage( self.socket, self.action + " is already taken, please chooses another name!", ClientMessage.MESSAGE_TYPE_ROOM )]

        oldName = clients[self.socket].clientName
        clients[self.socket].clientName = self.action

        return [
            ClientMessage( self.socket, oldName + " is now known as " +self.action, ClientMessage.MESSAGE_TYPE_ALL_OTHER, False ),
            ClientMessage( self.socket, "You are now known as "+self.action, ClientMessage.MESSAGE_TYPE_SELF )
        ]


class ClientActionDispatcher( ClientCommand ):

    commands = {
        "help": ClientActionHelp,
        "go": ClientActionGo,
        "talk": ClientActionTalk,
        "room": ClientActionRoom,
        "rename": ClientActionRename
    }

    def __init__( self, socket, message ):
        super().__init__( socket )

        self.message = message

    def RunCommand( self, clients, dungeon ):

        followUpCommands = [ ]

        user_input = self.message.split( ' ' )
        command = user_input[ 0 ].lower()
        action = ""

        if command != "help" and len( user_input ) < 2 or command not in self.commands:
            return [ ClientMessage( self.socket, "Invalid command", ClientMessage.MESSAGE_TYPE_SELF ) ]

        if len( user_input ) >= 2:
            action = ' '.join( user_input[ 1: ] )

        return self.commands[ command ]( self.socket, action ).RunCommand( clients, dungeon )
