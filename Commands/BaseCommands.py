class CommandBase:
    def __init__(self, socket):
        self.socket = socket

class ClientCommand(CommandBase):

    def RunCommand( self, clients ):
        """ Runs the command returning a list of follow up commands

        :param clients:     list of current active clients
        :return:            a list of follow up commands.
        """
        pass

class ClientAction(ClientCommand):

    def __init__(self, socket, action):
        super().__init__(socket)
        self.action = action