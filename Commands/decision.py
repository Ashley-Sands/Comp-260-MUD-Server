from Commands.message import *

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
