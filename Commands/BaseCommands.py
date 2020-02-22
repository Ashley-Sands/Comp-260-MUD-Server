class CommandBase:
    def __init__(self, socket):
        self.socket = socket

class ClientCommand(CommandBase):

    def RunCommand( self, clients, dungeon ):
        """ Runs the command returning a list of follow up commands

        :param clients:     list of current active clients
        :param dungeon:     The active dungeon for this game
        :return:            a list of follow up commands.
        """
        pass

class ClientAction(ClientCommand):

    def __init__(self, socket, action):
        super().__init__(socket)
        self.action = action

    @staticmethod
    def ActionHelp():
        return ""
