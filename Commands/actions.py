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

class ClientActionAttackUser( ClientAction ):

    def RunCommand( self, clients, dungeon ):

        if self.action == clients[self.socket].clientName:
            return [ ClientMessage( self.socket, " Don't hurt yourself... ", ClientMessage.MESSAGE_TYPE_SELF ) ]

        clientToAttack = None
        clientToAttackSocket = None
        for c in clients:
            if c is not self.socket and clients[c].clientName == self.action and clients[c].currentRoom == clients[self.socket].currentRoom:
                clientToAttack = clients[c]
                clientToAttackSocket = c
                break

        if clientToAttack is None:
            return [ ClientMessage( self.socket, self.action + " not found in current room", ClientMessage.MESSAGE_TYPE_SELF ) ]

        attacker_name = clients[self.socket].clientName
        victim_name = clientToAttack.clientName

        weapon = clients[self.socket].item
        defence_weapon = clientToAttack.item

        clientAlive, damageGiven, damageTaken = clientToAttack.attack( weapon, clientToAttack )
        selfDeaded = False

        # apply the damage to the two players
        clientToAttack.takeDamage(int(damageGiven))
        clients[self.socket].takeDamage(int(damageTaken))

        messages = [] # list of tuples. tuple layout (message, message type, [(optional) display from in message, [(optional)ignore client name]] )

        if not clientAlive: # that was easy there deaded

            messages.append( ("You killed "+victim_name, ClientMessage.MESSAGE_TYPE_SELF, False) )
            messages.append( (attacker_name+" killed "+victim_name, ClientMessage.MESSAGE_TYPE_ALL_OTHER_EXCEPT, False, victim_name) )
            messages.append( (attacker_name+" killed You", ClientMessage.MESSAGE_TYPE_PRIVATE, False, victim_name) )
            # add a decision to the victim so they have to reset the game now they have been killed
            clientToAttack.pendingAction = ClientNewGame(clientToAttackSocket)

        else:   # they put up a bit of a fight, as a result you take damage as well

            clients[ self.socket ].takeDamage( damageTaken )
            messages.append( (victim_name + " put up a bit of fight, as a result you have taken " + str(int(damageTaken)) + " damage", ClientMessage.MESSAGE_TYPE_SELF, False) )
            messages.append( (attacker_name + " attacked " + victim_name, ClientMessage.MESSAGE_TYPE_ALL_OTHER_EXCEPT, False, victim_name) )
            messages.append( (attacker_name + " attacked you with a " + weapon.name + " causing "+ str(int(damageGiven)) +" damage.", ClientMessage.MESSAGE_TYPE_PRIVATE, False, victim_name) )


        if selfDeaded:  # you got your ass handed to ya.
            messages.append( (victim_name +" killed You", ClientMessage.MESSAGE_TYPE_SELF, False ) )
            messages.append( ( attacker_name + " was killed by " + victim_name,
                                            ClientMessage.MESSAGE_TYPE_ALL_OTHER_EXCEPT, False, victim_name ) )
            messages.append( ("You put up a good fight and managed to deliver a fatal blow to your attackers" 
                              " head with you "+defence_weapon.name + " resulting in instance death\n"
                              " ** There's blood everywhere **\nlets hope the zombies don't smell that",
                              ClientMessage.MESSAGE_TYPE_PRIVATE, False, victim_name ) )
            # give the attack the option to start again
            clients[self.socket].pendingAction = ClientNewGame(self.socket)
        else:
            messages.append( (" But you put a fight and managed to defend your self. ("+str(attacker_name)+" lost "+str(int(damageTaken))+" hp) ",
                              ClientMessage.MESSAGE_TYPE_PRIVATE, False, victim_name) )

        # build the messages to each endpoint into a single message for each
        msg = {}            # dict of tuple (same as messages tuple)
        client_msgs = []    # list of final messages

        for m in messages:
            if m[1] in msg:
                msg[ m[1] ][0] = msg[ m[1] ][0] + "\n" + m[0]
            else:
                msg[ m[1] ] = list(m)

        for m in msg:
            client_msgs.append( ClientMessage(self.socket, *msg[m]) )

        return client_msgs

class ClientActionDispatcher( ClientCommand ):

    commands = {
        "help": ClientActionHelp,
        "go": ClientActionGo,
        "talk": ClientActionTalk,
        #"whisper": ClientActionWhisper,
        "room": ClientActionRoom,
        "rename": ClientActionRename,
        "search": ClientActionSearch,
        "attack": ClientActionAttackUser
        #"graffiti": ClientActionGraffiti
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

