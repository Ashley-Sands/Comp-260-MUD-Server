import Commands.actions as act
from Commands.message import *

class ClientContinue(ClientDecisions):

    def Decision( self, clients, dungeon, decision ):
        if decision != "":
            return True, act.ClientActionHelp( self.socket, "options" ).RunCommand( clients, dungeon )
        else:
            return True, [ClientMessage(self.socket, "Enter anything to continue", ClientMessage.MESSAGE_TYPE_SELF)]




class ClientCollectItem(ClientDecisions):

    def __init__(self, socket, item):
        super().__init__(socket)
        self.item = item

    def ActionDesc( self ):
        return "do you 'take' the item or 'leave' the item"

    def Decision( self, clients, dungeon, decision ):
        """

        :param clients:
        :param dungeon:
        :param decision:
        :return: tuple (was the decision successful, follow up commands)
        """
        if decision == "take":
            clients[self.socket].collectItem(self.item, dungeon.roomMap[clients[self.socket].currentRoom])
            return True, \
                   [ ClientMessage( self.socket, "You have chosen to take the "+self.item.name, ClientMessage.MESSAGE_TYPE_SELF, False ) ]
        elif decision == "leave":
            return True, \
                   [ ClientMessage( self.socket, "You have chosen to leave the "+self.item.name+". Good luck finding that again!", ClientMessage.MESSAGE_TYPE_SELF, False ) ]
        else:
            return False, \
                   [ ClientMessage( self.socket, "Decision not found\n" + self.ActionDesc(), ClientMessage.MESSAGE_TYPE_SELF, False ) ]

class ClientNewGame(ClientDecisions):

    def __init__(self, socket):
        super().__init__(socket)

    def ActionDesc( self ):
        return "You have been kill, 'new' game?"

    def Decision( self, clients, dungeon, decision ):

        if decision == "yes" or decision == "new" or decision == "y":
            return False, \
                   [ ClientMessage( self.socket, "Work in progress\n", ClientMessage.MESSAGE_TYPE_SELF, False ) ]
        else:
            return False, \
                   [ ClientMessage( self.socket, "Decision not found\n" + self.ActionDesc(), ClientMessage.MESSAGE_TYPE_SELF, False ) ]
