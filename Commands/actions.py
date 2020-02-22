from Commands.message import *
from Commands.decision import *
import random

class ClientActionHelp( ClientAction ):

    def __init__(self, socket, action):
        super().__init__(socket, action)

        self.help_func = { "location" : self.help_room,
                           "health": self.help_health,
                           "options": self.help_options
                           }

        self.help_description = { "location": "Get current location",
                                  "health": "Get current health",
                                  "options": "get current options"
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

    def ActionHelp( self, name ):
        return "**No one can here you screams down here**"

    def default_help( self ):

        help = "Type help [action] for more info \n[Actions]\n"

        # list action help
        for ha in ClientActionDispatcher.commands:
            help += "'"+ha+"'\n"

        # list other help
        for hd in self.help_description:
            help += "'"+hd+"'\n"

        return "HHHHHHHHHHHHHEEEEEEEEEEEEEEELLLLLLLLLLLLLLPPPPPPPPPPPP!\n" \
               "**You hear a faint whisper cut through the gloom**\n\n" + help

    def help_room( self, clients, dungeon ):
        return "While stareing blankly throught the dark gloomy room you notice that\n" \
               "someone has writen '"+clients[self.socket].currentRoom.upper()+"' in blood on the wall"

    def help_health( self, clients, dungeon ):
        return "Remaining Health: "+ str(clients[self.socket].health)

    def help_options( self, clients, dungeon ):
        findItemChance = dungeon.roomMap[ clients[self.socket].currentRoom ].searchChance()

        otherClients = ""
        clientCountInRoom = 0
        for c in clients:
            if c is not self.socket and clients[c].currentRoom == clients[self.socket].currentRoom:
                otherClients += "- "+clients[c].clientName+"\n"
                clientCountInRoom += 1

        if clientCountInRoom > 0:
            otherClients = "\nand see "+str(clientCountInRoom)+" other user lerking in the darkness\n" + otherClients


        actions = "\n\nDo you\n'go' throught a bloody door"
        actions += "\n'search' the room for items ("+ str(findItemChance * 100) + "% chance)"

        weapon = "bear hands"
        if clients[self.socket].item is not None:
            weapon = clients[self.socket].item.name
        actions += "\n'attack' another client with your "+weapon

        return dungeon.DisplayRoomOptions( clients[self.socket].currentRoom ) + otherClients + actions


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


class ClientActionSearch(ClientAction):

    def RunCommand( self, clients, dungeon ):

        currentRoom = clients[self.socket].currentRoom
        foundItem = dungeon.roomMap[currentRoom].searchForItem()
        message = "you did not find an item this time"

        if foundItem is not None:
            message = "You found a "+foundItem.name + "\n" + foundItem.getInfo()
            clients[self.socket].pendingAction = ClientCollectItem(self.socket, foundItem)
            message += "\n" + clients[self.socket].pendingAction.ActionDesc()

        return [ ClientMessage( self.socket, message, ClientMessage.MESSAGE_TYPE_SELF, False ) ]


class ClientActionDispatcher( ClientCommand ):

    commands = {
        "help": ClientActionHelp,
        "go": ClientActionGo,
        "talk": ClientActionTalk,
        "room": ClientActionRoom,
        "rename": ClientActionRename,
        "search": ClientActionSearch
    }

    def __init__( self, socket, message ):
        super().__init__( socket )

        self.message = message

    def RunCommand( self, clients, dungeon ):

        followUpCommands = [ ]

        user_input = self.message.split( ' ' )
        command = user_input[ 0 ].lower()
        action = ""

        # check we are not waiting for a dicision to be made
        if clients[self.socket].pendingAction != None:
            success, followUps = clients[ self.socket ].pendingAction.Decision( clients, dungeon, command )
            if success:
                clients[self.socket].pendingAction = None
            return followUps

        if command != "help" and len( user_input ) < 2 or command not in self.commands:
            return [ ClientMessage( self.socket, "Invalid command", ClientMessage.MESSAGE_TYPE_SELF ) ]

        if len( user_input ) >= 2:
            action = ' '.join( user_input[ 1: ] )

        return self.commands[ command ]( self.socket, action ).RunCommand( clients, dungeon )

