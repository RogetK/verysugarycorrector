from pynput import keyboard
import socket, serial

host = "127.0.0.1"
port = 1235

stri = ""

ser = serial.Serial("/dev/ttyAMA0", 115200)

punctuation = ("Key.space", "Key.enter", "','", "'.'", "'!'", "'?'", "'''", "':'", "';'""'('", "')'", "'-'", "'_'", "'='", "'+'")

punctuation2 = {"Key.space":32, "Key.enter":"10", "','": 44, "'.'": 46, "'!'": 33, "'?'": 63, "'''": 39, "':'": 58, "';'": 59, "'('": 40, "')'": 41, "'-'": 45, "'_'": 95, "'='": 61, "'+'": 43}

def write_punct2(key):
    if str(key) in punctuation2.keys:
        code = punctuation2[str(key)]
        ser.write(bytearray([17,code,18,code]))
        ser.flush()

def write_punct(key):
    if str(key) == "Key.space":
        ser.write(bytearray([17,32,18,32]))
    elif str(key) == "Key.enter":
        ser.write(bytearray([17,10,18,10]))
    elif str(key) == "','":
        ser.write(bytearray([17,44,18,44]))
    elif str(key) == "'.'":
        ser.write(bytearray([17,46,18,46]))
    elif str(key) == "'!'":
        ser.write(bytearray([17,33,18,33]))
    elif str(key) == "'?'":
        ser.write(bytearray([17,63,18,33]))
    elif str(key) == "'''":
        ser.write(bytearray([17,39,18,33]))
    elif str(key) == "':'":
        ser.write(bytearray([17,58,18,33]))
    elif str(key) == "';'":
        ser.write(bytearray([17,59,18,33]))
    elif str(key) == "'('":
        ser.write(bytearray([17,40,18,33]))
    elif str(key) == "')'":
        ser.write(bytearray([17,41,18,33]))
    elif str(key) == "'-'":
        ser.write(bytearray([17,45,18,33]))
    elif str(key) == "'_'":
        ser.write(bytearray([17,95,18,33]))
    elif str(key) == "'='":
        ser.write(bytearray([17,61,18,33]))
    elif str(key) == "'+'":
        ser.write(bytearray([17,43,18,33]))
    ser.flush()
    

def on_press(key):
    global stri
    try:
        #print(key)
        #stri += key.char
        if str(key) in punctuation:
            print("{}".format(stri))
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.sendto(stri.encode(), (host,port))
                #text, source = s.recvfrom(1024)
                num, source2 = s.recvfrom(1024)
                #text = text.decode()
                num = int(num.decode())
                #print("suggestion 0: '{}'".format(text))
                print("num: {}".format(repr(num)))
                text = stri
                for i in range(0, num):
                    sugg, sourcen = s.recvfrom(1024)
                    sugg = sugg.decode()
                    if i == 0:
                        text = sugg
                    print("Suggestion {}: '{}'".format(i, sugg))
                if text != stri and stri != "":
                    for i in range(0,len(stri)):
                        ser.write(bytearray([17,8,18,8]))
                        ser.flush()
                    for char in text:
                        ser.write(bytearray([17,]))
                        ser.write(char.encode())
                        ser.write(bytearray([18,]))
                        ser.write(char.encode())
                        ser.flush()
                write_punct2(key)
                stri = ""
                print("stri: {}".format(stri))
            stri = ""
            print("stri: {}".format(stri))
        elif str(key) == "Key.backspace":
            ser.write(bytearray([17,8,18,8]))
            ser.flush()
        else:
            stri += key.char
            print("stri: {}".format(stri))
            ser.write(bytearray([17,]))
            ser.write(key.char.encode())
            ser.write(bytearray([18,]))
            ser.write(key.char.encode())
            ser.flush()
            
            print('alphanumeric key {0} pressed'.format(str(key)))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))
        

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
