
class Client:

    def __init__(self, client_name):
        self.clientName = client_name
        self.currentRoom = ""
        self.item = ""
        self.health = 100

        self.is_zombie = False  # when a user disconnects they become zombies :)

    def is_alive( self ):
        return self.health > 0

    def takeDamage( self, damage ):
        """ applies damage to the client

        :param damage:
        :return: true if the client dies
        """
        self.health -= damage

        return not self.is_alive()

