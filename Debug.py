__author__ = 'Wild_Doogy'

from threading import Thread
import time
import sys
import socket



def log(*args):
    print "[Debug]",
    print time.strftime("%c"),
    print " ",
    for arg in args:
        print arg,
    print ""


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
            command = raw_input()
            if command.upper() == "Q":
                import os
                os._exit(1)
            elif command.upper() == "S":
                message = ""
                for obj in self.watch_list:
                    obj_attributes = [a for a in dir(obj) if not a.startswith('_')]
                    try:
                        message += obj.__class__.__name__
                    except Exception as e:
                        log(e)

                    for attribute in obj_attributes:
                        try:
                            real_attribute = getattr(obj, attribute)
                        except AttributeError as e:
                            log(e)
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
                            pass
                log("Status:\n", message)
            elif len(command):
                if command.upper()[0] == "$":
                    try:
                        result = eval(command[1:])
                        log(command[1:], "$", result)
                    except:
                        log(sys.exc_info())
                elif command.upper()[0] == "#":
                    try:
                        exec command[1:]
                    except:
                        log(sys.exc_info())


