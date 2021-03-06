__author__ = 'Wild_Doogy'

from threading import Thread
import time
import sys
import socket


class Debug(Thread):
    def __init__(self, objects_to_watch):
        """

        :return:
        """
        Thread.__init__(self)
        self.go = True
        self.watch_list = objects_to_watch
        self.socket = self.socket_init()
        self.socket_start(self.socket, (self.getlocalip(), 9092))
        self.messages = []

    def log(self, *args):
        msg = "[Debug] "
        msg += str(time.strftime("%c")) + " "
        for arg in args:
            msg += str(arg)
        self.messages.append(msg)

    def socket_init(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def socket_start(self, my_socket, address):
        """

        :param my_socket: A socket object to start listening on
        :type my_socket: socket.socket
        :param address: The address to start listening on. Format: ("localhost", 80)
        :type address: tuple of (str, int)
        :return:
        """
        my_socket.bind(address)
        my_socket.listen(50)

    def socket_accept(self, my_socket):
        """

        :param my_socket: A socket to accept connections on
        :type my_socket: socket.socket
        :return:
        """
        return my_socket.accept()

    def getlocalip(self):
        import os

        c4 = ""
        if os.sys.platform == "win32":
            back = os.popen("ipconfig /all")
            cmd = back.read(2000)
            cmd2 = cmd[cmd.find("IP Address"):cmd.find("IP Address") + 70]
            cmd3 = cmd2[cmd2.find(":") + 2:cmd2.find(":") + 19]
            c4 = cmd3[0:cmd3.find(" ") - 2]
        elif os.sys.platform == "linux2":
            back = os.popen("ifconfig")
            cmd = back.read(2000)
            cmd2 = cmd[cmd.find("Ethernet"):cmd.find("Ethernet") + 300]
            cmd3 = cmd2[cmd2.find("inet addr:") + 10:cmd2.find("inet addr:") + 50]
            c4 = cmd3[0:cmd3.find(" ")]
        if c4 != "":
            return c4
        else:
            return "localhost"

    def run(self):
        while self.go:
            try:
                client, address = self.socket_accept(self.socket)
                command = ""
                while 1:
                    try:
                        command = client.recv(10000)
                        if command.upper() == "Q":
                            import os
                            os._exit(1)
                        elif command.upper() == "N":
                            for i in range(30):
                                client.send(self.messages.pop() + "\n")
                        elif command.upper() == "S":
                            message = ""
                            for obj in self.watch_list:
                                obj_attributes = [a for a in dir(obj) if not a.startswith('_')]
                                try:
                                    message += obj.__class__.__name__
                                except Exception as e:
                                    self.log(e)

                                for attribute in obj_attributes:
                                    try:
                                        real_attribute = getattr(obj, attribute)
                                    except AttributeError as e:
                                        self.log(e)
                                        break
                                    try:
                                        max = 5
                                        if type(real_attribute) == str:
                                            max = 100
                                        if len(real_attribute) > max:
                                            message += "\tLen of {0}:{1}\n".format(attribute, len(real_attribute))
                                        else:
                                            message += "\t{0}:{1}\n".format(attribute, str(real_attribute))
                                    except Exception as e:
                                        self.log(e)
                            self.log("Status:\n", message)
                        elif len(command):
                            if command.upper()[0] == "$":
                                try:
                                    result = eval(command[1:])
                                    self.log(command[1:], "$", result)
                                except:
                                    self.log(sys.exc_info())
                            elif command.upper()[0] == "#":
                                try:
                                    exec command[1:]
                                except:
                                    self.log(sys.exc_info())
                    except Exception as e:
                        self.log(e)
            except Exception as e:
                self.log(e)



if __name__ == "__main__":
    def getadd():
        local = getlocalip()
        host = raw_input("Type host, skip for " + str(local) + ":")
        if host == "":
            host = local
        port = raw_input("Type port, skip for 9092 :")
        if port:
            port = int(port)
        else:
            port = 9092
        address = (host, port)
        return address


    def getlocalip():
        import os
        if os.sys.platform == "win32":
            back = os.popen("ipconfig /all")
            cmd = back.read(2000)
            cmd2 = cmd[cmd.find("IP Address"):cmd.find("IP Address") + 70]
            cmd3 = cmd2[cmd2.find(":") + 2:cmd2.find(":") + 19]
            c4 = cmd3[0:cmd3.find(" ") - 2]
        if os.sys.platform == "linux2":
            back = os.popen("ifconfig")
            cmd = back.read(2000)
            cmd2 = cmd[cmd.find("Ethernet"):cmd.find("Ethernet") + 300]
            cmd3 = cmd2[cmd2.find("inet addr:") + 10:cmd2.find("inet addr:") + 50]
            c4 = cmd3[0:cmd3.find(" ")]
        if c4 != "":
            return c4
        else:
            return "localhost"


    def setup(address):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(address)
        return client


    class ThreadClass(Thread):
        def __init__(self):
            Thread.__init__(self)

        def run(self):
            pass


    def startclass():
        TClass = ThreadClass()
        TClass.start()
        return TClass


    def mainprog(client):
        i = 0
        while 1:
            i += 1
            try:
                client.send(raw_input())
                print client.recv(200000)
            except:
                print "Socket closed. Reconnecting."
                break


    while 1:
        client = setup(getadd())
        mainprog(client)
