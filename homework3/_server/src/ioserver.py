import logging
import re
import socket
import select
from _server._config import common

class IoServer(object):
    def __init__(self):
        self.host = common.ip_address
        self.port = common.port
        self.socket_object_list = []
        self.conn_handler_map = {}

    def run_server(self,pan):
        server_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_object.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        '''
        socket. setsockopt ( level, optname, value )
        Set the value of the given socket option (see the Unix manual pagesetsockopt(2)).
         The needed symbolic constants are defined in thesocket module (SO_* etc.). The 
         value can be an integer or a string representing a buffer. In the latter case 
         it is up to the caller to ensure that the string contains the proper bits (see 
         the optional built-in modulestruct for a way to encode C structures as strings).
        有三个参数：
        level：选项定义的层次。支持SOL_SOCKET、IPPROTO_TCP、IPPROTO_IP和IPPROTO_IPV6。
        optname：需设置的选项。
        value：设置选项的值。
        https://www.cnblogs.com/gangzilife/p/9766114.html
        '''

        server_object.setblocking(True)
        server_object.bind((self.host, self.port))
        server_object.listen(5)
        self.socket_object_list.append(server_object)

        while True:
            r, w, e = select.select(self.socket_object_list, [], [], 0.05)
            for sock in r:
                # 新连接到来，执行 handler的 __init__ 方法
                if sock == server_object:
                    conn, addr = server_object.accept()
                    self.socket_object_list.append(conn)
                    # 实例化handler类，即：类(conn)
                    self.conn_handler_map[conn] = pan(conn)
                    logging.info('new connection{} is coming'.format(addr))
                    continue

                # 新数据到来，执行 handler的 __call__ 方法
                handler_object = self.conn_handler_map[sock]
                # print(handler_object)
                # 执行handler类对象的 execute 方法，如果返回False，则意味关闭服务端与客户端的连接
                result = handler_object._execute()
                if not result:
                    self.socket_object_list.remove(sock)
                    del self.conn_handler_map[sock]
        sock.close()

