from Commands.BaseCommands import *

class ClientMessage(CommandBase):

    MESSAGE_TYPE_SELF                = 0     # send message to this socket only
    MESSAGE_TYPE_ALL                 = 1     # send message to all clients including this client/socket
    MESSAGE_TYPE_ALL_OTHER           = 2     # send message to all clients excluding this client/socket
    MESSAGE_TYPE_ROOM                = 3     # send message to all clients with in the same room
    MESSAGE_TYPE_PRIVATE             = 4     # Send a private message to client
    MESSAGE_TYPE_ALL_OTHER_EXCEPT    = 5     # Send a private message all clients except 1 and excluding this client/socket

    def __init__(self, socket, message, message_type, display_client_name=True, privateClient=None):
        """
        :param socket:          This clients sockets
        :param message:         The message to be sent
        :param message_type:    Who to send the message to (MESSAGE_TYPE_SELF, MESSAGE_TYPE_ALL or MESSAGE_TYPE_ALL_OTHER)
        """
        super().__init__(socket)
        self.message = message
        self.message_type = message_type
        self.display_name = display_client_name
        self.privateClient = privateClient
        self.message_commands = { self.MESSAGE_TYPE_SELF:               self.message_self,
                                  self.MESSAGE_TYPE_ALL:                self.message_all,
                                  self.MESSAGE_TYPE_ALL_OTHER:          self.message_all_other,
                                  self.MESSAGE_TYPE_ROOM:               self.message_room,
                                  self.MESSAGE_TYPE_ALL_OTHER_EXCEPT:   self.message_all_other,
                                  self.MESSAGE_TYPE_PRIVATE:            self.message_private
                                  }

    def get_prefix( self, clients ):

        if not self.display_name:
            return ""

        if clients is not None:
            return clients[self.socket].clientName + ": "
        else:
            return "Server says "


    def senMessage( self, send_message_func, clients ):

        if self.message_type == self.MESSAGE_TYPE_PRIVATE or self.message_type == self.MESSAGE_TYPE_ALL_OTHER_EXCEPT:
            self.message_commands[self.message_type](send_message_func, clients, self.privateClient)
        else:
            self.message_commands[self.message_type](send_message_func, clients)

    def message_self( self, send_message_func, clients ):
        if self.socket in clients:
            send_message_func(self.socket, self.get_prefix(None) + self.message)

    def message_all( self, send_message_func, clients ):
        for c in clients:
            send_message_func(c, self.get_prefix(clients)+self.message)

    def message_all_other( self, send_message_func, clients, ignoreClient=None ):

        clientExist = self.socket in clients
        from_client = clients[self.socket].clientName

        for c in clients:
            # skip the ignored client :)
            if clients[c].clientName == ignoreClient:
                continue

            if not clientExist or ( clientExist and c is not self.socket ):
                send_message_func(c, self.get_prefix(clients) + self.message)

    def message_room( self, send_message_func, clients ):

        if self.socket not in clients:
            return

        client_room_id = clients[self.socket].currentRoom
        from_client = clients[self.socket].clientName

        for c in clients:
            if c is not self.socket and clients[c].currentRoom == client_room_id:
                send_message_func( c, self.get_prefix(clients) + self.message )

    def message_private( self , send_message_func, clients, client_name):

        foundClientSocket = None

        for c in clients:
            if clients[c].clientName == client_name:
                foundClientSocket = c
                break

        if foundClientSocket is None:
            return  # client not found.

        if client_name in clients:
            send_message_func( foundClientSocket, self.get_prefix(clients) + self.message  )

