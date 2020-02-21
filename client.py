
class Client:

    def __init__(self, client_name):
        self.clientName = client_name
        self.currentRoom = "room 0"
        self.item = ""
        self.health = 100

    def is_alive( self ):
        return self.health > 0

    def takeDamage( self, damage ):
        """ applies damage to the client

        :param damage:
        :return: true if the client dies
        """
        self.health -= damage

        return not self.is_alive()

class ZombieClient(Client):

    def __int__(self, client):
        self.clientName = "Zombie"+client.clientName
        self.currentRoom = client.currentRoom;
        self.item = client.item
        self.health = client.health / 2.0
