import threading, os


def open_gui():
    global path
    os.system('\"'+path+'words_gui.py'+'\"')

def record_input():
    global path
    os.system('\"'+path+'words_input.py'+'\"')

path = os.path.realpath(__file__)
path = path[:path.rfind('\\')+1]

thread_1 = threading.Thread(target = open_gui)
thread_2 = threading.Thread(target = record_input)
thread_1.start()
thread_2.start()