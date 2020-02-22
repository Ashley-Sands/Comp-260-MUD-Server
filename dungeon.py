from room import Room, Item
import copy
import random

class Dungeon:
    def __init__(self):
        # there mey be dupes in items as the current help is random to give variants
        items = [
            Item("Axe", 30, 35, 0.8), Item("Axe", 30, 35, 0.8), Item("Axe", 30, 35, 0.8),
            Item("Screwdriver", 20, 25, 0.3), Item("Screwdriver", 20, 25, 0.3),
            Item("Screwdriver", 20, 25, 0.3), Item("Screwdriver", 20, 25, 0.3),
            Item("Hammer", 35, 45, 0.6), Item("Hammer", 35, 45, 0.6), Item("Hammer", 35, 45, 0.6),
            Item("Sledgehammer", 35, 45, 0.9),
            Item("Brick", 65, 45, 0.85), Item("Brick", 65, 45, 0.85), Item("Brick", 65, 45, 0.85),
            Item("Flip Knife", 80, 60, 0.625), Item("Flip Knife", 80, 60, 0.625),
            Item("Machete", 150, 80, 0.95),
        ]

        self.roomMap = {
            "room 0": Room("room 0", "You are standing in the entrance hall", "room 1", "",  "", "", self.GetRandomItems(items, 1) ),
            "room 1": Room("room 1", "You are in room 1","", "room 0", "room 3", "room 2", self.GetRandomItems(items, 4)),
            "room 2": Room("room 2", "You are in room 2", "room 4", "", "", "", self.GetRandomItems(items, 8)),
            "room 3": Room("room 3", "You are in room 3", "", "", "", "room 1", self.GetRandomItems(items, 3)),
            "room 4": Room("room 4", "You are in room 4", "", "room 2", "room 5", "", self.GetRandomItems(items, 4)),
            "room 5": Room("room 5", "You are in room 5", "", "room 1", "", "room 4", self.GetRandomItems(items, 6))
        }

    def GetRandomItems( self, items, maxItemCount ):

        itemCount = random.randint(0, maxItemCount)
        roomItems = []

        for i in range(itemCount):
            roomItems.append( random.choice( copy.deepcopy( items ) ) )

        return roomItems


    def DisplayRoomOptions(self, roomName):
        """ displays the current room and available exits.

        :return: the message that to be dusplayed to the client execute the command
        """

        exits = ["NORTH", "SOUTH", "EAST", "WEST"]
        exitStr = ''

        if roomName.lower() not in self.roomMap:
            return "Room does not exist " + roomName

        for i in exits:
            if self.roomMap[roomName].hasExit(i.lower()):
                exitStr += i + "\n"

        return self.roomMap[roomName].desc + " \nExits\n" + exitStr


    def isValidMove(self, direction, roomName):
        return roomName.lower() in self.roomMap and self.roomMap[roomName].hasExit(direction)

    def MovePlayer(self, direction, roomName):
        if self.isValidMove(direction, roomName):

            if direction == "north":
                roomName = self.roomMap[roomName].north
            elif direction == "south":
                roomName = self.roomMap[roomName].south
            elif direction == "east":
                roomName = self.roomMap[roomName].east
            elif direction == "west":
                roomName = self.roomMap[roomName].west

            return True, roomName

        else:
            return False, "Invalid"
