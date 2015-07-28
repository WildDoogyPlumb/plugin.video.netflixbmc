__author__ = 'Wild_Doogy'

from threading import Thread
import time
import sys



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


