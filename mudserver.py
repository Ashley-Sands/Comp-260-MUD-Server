import sys
import socket
import threading
import datetime

from queue import *
from Commands.commands import *
from client import *
from dungeon import *

messageQueue = Queue()
activeDungeon = Dungeon()

clientIndex = 0
currentClients = {}
currentClientsLock = threading.Lock()

zombieIndex = 0
zombieClients = {}

deadEntitiesIndex = 0
deadEntities = {}

host = ''
port = 0

def get_entity( entity_type, entity_key ):
    """

    :param entity_type:         The Type of entity (See Entity for type constants)
    :param entity_key:          The key for the entity. (for default and zombies this is there name else it is the socket related to the client) leave None to return all
    :return:                    None if not found
    """
    entities = {Entity.ENTITY_DEFAULT: deadEntities, Entity.ENTITY_CLIENT: currentClients, Entity.ENTITY_ZOMBIE: zombieClients}
    if entity_key is None and entity_type in entities:
        return entities[ entity_type ]
    elif entity_type in entities and entity_key in entities[entity_key]:
        return entities[ entity_type ][ entity_key ]
    else:
        return None


def debug_print(text):
    print(str(datetime.datetime.now()) + ':' + text)


def sendString(socket,str):

    str = ''.join(["-"*20]) + "\n" + str
    data= bytes(str,'utf-8')
    try:
        if socket.send(len(data).to_bytes(2, byteorder='big')) == 0:
            raise socket.error

        if socket.send(data) == 0:
            raise socket.error
    except:
        messageQueue.put( ClientLost( socket ) )

def clientReceive(sock):

    clientValid = True

    clientName = ''

    currentClientsLock.acquire()

    if sock in currentClients:
        clientName = currentClients[sock].clientName
    else:
        clientName = 'N/A'
        currentClientsLock.release()
        return


    currentClientsLock.release()

    debug_print(clientName + ':clientReceive running')

    while clientValid == True:
        try:
            data = sock.recv(2)

            currentClientsLock.acquire()

            if sock in currentClients:
                clientName = currentClients[sock].clientName
            else:
                clientName = 'N/A'
                clientValid = False
            currentClientsLock.release()

            if len(data) == 0:
                # on OSX, 'closed' sockets send 0 bytes, so trap this
                raise socket.error

            size = int.from_bytes(data, byteorder='big')

            data = sock.recv(size)

            if len(data) > 0:
                incoming_msg = data.decode('utf-8')

                debug_print('recv:' + clientName + ':' + incoming_msg)

                for act in ClientActionDispatcher( sock, incoming_msg).RunCommand(currentClients, activeDungeon):
                    messageQueue.put( act )
                    # messageQueue.put(ClientMessage(sock, incoming_msg, ClientMessage.MESSAGE_TYPE_ALL_OTHER) )

        except socket.error:
            debug_print(clientName +':clientReceive - lost client')
            clientValid = False
            messageQueue.put(ClientLost(sock))


def acceptClients(serversocket):
    debug_print('acceptThread running')
    while(True):
        (clientsocket, address) = serversocket.accept()
        messageQueue.put( ClientJoined( clientsocket ) )

        while clientsocket not in currentClients:   # wait for the user to be added to users
            pass

        messageQueue.put(ClientJoined(clientsocket).welcome()[0])
        currentClients[clientsocket].pendingAction = ClientContinue(clientsocket)





def handleClientLost(command):
    global zombieIndex

    currentClientsLock.acquire()
    try:

        for c in command.RunCommand(currentClients):
            messageQueue.put( c )

        debug_print('Removing lost client:' + currentClients[command.socket].clientName)

        zombieClients["zombie_"+ str(zombieIndex)] = ZombieClient(currentClients[command.socket])
        zombieIndex += 1

        del currentClients[command.socket]
    except:
        pass

    currentClientsLock.release()


def handleClientJoined(command):
    global clientIndex

    clientName = 'client-' + str(clientIndex)
    clientIndex += 1

    currentClientsLock.acquire()

    currentClients[command.socket] = Client(clientName)

    for c in command.RunCommand( currentClients ):
        messageQueue.put( c )

    currentClientsLock.release()

    message = 'Joined server as:' + clientName
    debug_print('send:' + clientName + ':' + message)

    sendString(command.socket, message)

    thread = threading.Thread(target=clientReceive, args=(command.socket,))
    thread.start()


def handleClientMessage(command):

    currentClientsLock.acquire()

    clientName = "None"

    if command.socket in currentClients:
        clientName = currentClients[ command.socket ].clientName

    command.senMessage( sendString, currentClients )

    currentClientsLock.release()

    debug_print('send:' + clientName + ':'+command.message)

def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host = 'localhost'
    port = 9000

    if len(sys.argv) > 1:
        host = sys.argv[1]

        if len(sys.argv) > 2:
            port = sys.argv[2]

    try:
        serversocket.bind((host, port))
    except socket.error as err:
        debug_print('Can\'t start server, is another instance running?')
        debug_print(format(err))
        exit()

    debug_print(host +':' + str(port))

    serversocket.listen(5)

    thread = threading.Thread(target=acceptClients,args=(serversocket,))
    thread.start()

    while True:

        if messageQueue.qsize()>0:
            command = messageQueue.get()

            if isinstance(command, ClientJoined):
                handleClientJoined(command)

            if isinstance(command, ClientLost):
                handleClientLost(command)

            if isinstance(command, ClientMessage):
                handleClientMessage(command)


if __name__ == '__main__':
    main()