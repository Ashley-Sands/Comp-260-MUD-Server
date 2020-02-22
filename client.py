import random

class Client:

    def __init__(self, client_name):
        self.clientName = client_name
        self.currentRoom = "room 0"
        self.item = None
        self.health = 100
        self.defence = 0.5

    def is_alive( self ):
        return self.health > 0

    def takeDamage( self, damage ):
        """ applies damage to the client

        :param damage:
        :return: true if the client dies
        """
        self.health -= damage

        return not self.is_alive()

    def collectItem( self, item, room ):
        # take the item from the room
        room.remove(item)

        # drop our current item in room
        if self.item is not None:
            self.item.itemBrokenCallback.remove(self.itemBroken)
            room.append(self.item)

        self.item = item
        self.item.itemBrokenCallback.append( self.itemBroken )

    def itemBroken( self ):
        self.item = None


class ZombieClient(Client):

    def __int__(self, client):
        self.clientName = "Zombie"+client.clientName
        self.currentRoom = client.currentRoom;
        self.item = client.item
        self.health = client.health / 2.0
        self.defence = random.uniform(0.2, 0.5)

