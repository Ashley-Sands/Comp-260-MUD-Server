import random
from room import Item
from Commands.message import *


class Entity:

    def __init__(self, client_name, current_room, item):
        self.clientName = client_name
        self.currentRoom = current_room
        self.item = item


class Client( Entity ):

    def __init__(self, client_name):

        self.bearHands = Item("Bare Knuckle", 10, 999, 0.23)  # default item

        super(Client, self).__init__( client_name, "room 0", self.bearHands )

        self.health = 100
        self.defence = 0.5
        self.pendingAction = None   # used for when a client needs to make a decisions

    def is_alive( self ):
        return self.health > 0

    def takeDamage( self, damage ):
        """ applies damage to the client

        :param damage:
        :return: true if the client dies
        """
        self.health -= damage

        return not self.is_alive()

    def attack( self, attackWithItem, victim):
        """returns tuple (is alive, damage taken, damage given)"""

        damageTaken, damageGiven = Item.getItemDamage(attackWithItem, victim)

        return damageTaken, damageGiven

    def collectItem( self, item, room ):
        # take the item from the room
        room.items.remove(item)

        # drop our current item in room
        if self.item is not None and self.itemBroken in self.item.itemBrokenCallback:
            self.item.itemBrokenCallback.remove(self.itemBroken)
            room.items.append(self.item)

        self.item = item
        self.item.itemBrokenCallback.append( self.itemBroken )

    def dropItem( self, room ):

        if self.item is None:
            return

        self.item.itemBrokenCallback.remove(self.itemBroken())
        self.item = self.bearHands

    def itemBroken( self ):
        self.item = self.bearHands


class ZombieClient(Client):

    def __int__(self, client):
        self.clientName = "Zombie"+client.clientName
        self.currentRoom = client.currentRoom;
        self.item = client.item
        self.health = client.health / 2.0
        self.defence = random.uniform(0.2, 0.5)

