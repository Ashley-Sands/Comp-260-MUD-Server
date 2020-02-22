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


class Item:

    def __init__( self, name, damage, maxHP, damageChance):
        self.name = name
        self.damage = damage
        self.maxHP = maxHP
        self.currentHP = maxHP * random.uniform(0.6, 1.0)
        self.damageChance = damageChance

