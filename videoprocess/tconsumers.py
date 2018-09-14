

sockets = {'bar': 'foo'}

def declare_socket(sessionID):
    global sockets
    sockets[sessionID] = 'UNKNOWN'
    print('declared')

def register_socket(sessionID, socket):
    global sockets
    # if(sessionID in sockets):
    #     socket.count += 1
    # else:
    #     socket.count = 1
    #     sockets[sessionID] = socket
    skt = seek_socket(sessionID)

    if(skt == 'UNKNOWN' or skt == 'NOTFOUND'):
        print('no')
        socket.count = 1
        sockets[sessionID] = socket
    else:
        print('there is')
        sockets[sessionID].count += 1

def seek_socket(sessionID):
    global sockets
    if(sessionID in sockets):
        return sockets.get(sessionID)
    else:
        return 'NOTFOUND'

def drop_socket(sessionID):
    global sockets
    socket = sockets.get(sessionID)
    print('skt.count = ', socket.count)
    if(socket.count > 1):
        socket.count -= 1
    else:
        sockets.pop(sessionID)