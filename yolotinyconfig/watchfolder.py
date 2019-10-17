#!/usr/bin/python
# -*- coding:UTF-8 -*-

import os
import time
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler

# reges = [r".*\.c", r".*\.h", r".*\.cpp"]

class MyHandler(RegexMatchingEventHandler):

   

    def __init__(self, regex_list=[r".*"],ignore_directories=True):
        super(MyHandler, self).__init__(regex_list)

    # def on_created(self, event):
     #   if event.is_directory:
      #      pass
       # else:
        #     if os.access(event.src_path, os.R_OK):
         #       print(event.event_type, event.src_path)
            #myCmd = './darknet detector test backup/rpi.data backup/rpi.cfg  backup/rpi_best.weights backup/'+event.src_path
            #os.system(myCmd)


    def on_deleted(self, event):
        if event.is_directory:
            pass
        else:
            if os.access(event.src_path, os.R_OK):
                    print(event.event_type, event.src_path)

    def on_modified(self, event):
        substring = "label"

        if event.is_directory:
            pass
        else:
            if os.access(event.src_path, os.R_OK) == True: 
                if substring in str(event.src_path):
                    print(event.event_type, event.src_path)
                    print (os.access(event.src_path, os.R_OK))
                    myCmd = './darknet detector test backup/rpi.data backup/rpi.cfg  backup/rpi_best.weights -thresh 0.70 '+event.src_path
                    os.system(myCmd)


    def on_moved(self, event):
        print("move", event.src_path, event.dest_path)

if __name__ == "__main__":
    reges = [r".*\.jpg"]
    event_handler = MyHandler(reges)
    #event_handler=MyHandler(patterns=[r".*\.jpg"],ignore_directories=True)
    observer = Observer()
    observer.schedule(event_handler, "./upload", recursive=True)
    observer.start()

    try:
        print("start my watch")
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()