import random

class Room:

    def __init__(self, name, desc, north, south, west, east, items):
        self.name = name
        self.desc = desc
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.items = items

    def hasExit(self,direction):
        if(direction == "north") and (self.north != ""):
            return True

        if (direction == "south") and (self.south != ""):
            return True

        if (direction == "east") and (self.east != ""):
            return True

        if (direction == "west") and (self.west != ""):
            return True

        return False

    def searchChance( self ):
        chance = (len(self.items) * 5) / 100

        if chance < 0.1:
            chance = 0.1
        elif chance > 0.9:
            chance = 0.9

        return chance

    def searchForItem( self ):

        chance = self.searchChance()
        itemId = random.randint(0, len(self.items))

        if random.random() <= chance:
            return self.items[itemId]
        else:
            return None

class Item:

    def __init__( self, name, damage, maxHP, damageChance):
        self.name = name
        self.damage = damage
        self.maxHP = maxHP
        self.currentHP = maxHP * random.uniform(0.6, 1.0)
        self.damageChance = damageChance
        self.itemBrokenCallback = []

    def Use( self, client ):
        """ use item against client (or zombie client)

        :param client:  the client to attack
        :return: tuple of damage to client, damage to self
        """

        damage = self.damage * (self.currentHP / self.maxHP)
        selfDamage = damage * random.uniform(0.0, client.defence)
        damage -= selfDamage

        self.currentHP -= random.randrange(1, 50)

        if self.currentHP <= 0:
            for cb in self.itemBrockenCallback:
                cb()

        return damage, selfDamage