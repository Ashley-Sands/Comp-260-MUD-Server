from room import Room


class Dungeon:
    def __init__(self):

        self.roomMap = {
            "room 0": Room("room 0", "You are standing in the entrance hall\nAll adventures start here", "room 1", "",  "", ""),
            "room 1": Room("room 1", "You are in room 1","", "room 0", "room 3", "room 2"),
            "room 2": Room("room 2", "You are in room 2", "room 4", "", "", ""),
            "room 3": Room("room 3", "You are in room 3", "", "", "", "room 1"),
            "room 4": Room("room 4", "You are in room 4", "", "room 2", "room 5", ""),
            "room 5": Room("room 5", "You are in room 5", "", "room 1", "", "room 4")
        }

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

    def MovePlayer(self,direction, roomName):
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
