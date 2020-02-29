class CommandBase:
    def __init__(self, socket):
        self.socket = socket

# TODO: clients should become entities and be a dict or tuple [Clients, Zombies and Deaded things]
# Or pass in a function to get the client, zombie or deaded thing...


class ClientCommand(CommandBase):

    def __init__(self, socket): #, get_entity_func):
        super().__init__( socket )
        # self.GetEntity = get_entity_func

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

    def ActionHelp(self, name):
        return "No Help Available for "+name

class ClientDecisions(CommandBase):

    def __init__(self, socket):
        super().__init__(socket)

    def ActionDesc(self, name):
        return "No Help Available for "+name

    def Decision( self, clients, dungeon, action ):
        pass
