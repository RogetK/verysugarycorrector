from pynput import keyboard
import socket, serial

host = "127.0.0.1"
portAC = 1235
portWT = 1236

stri = ""

ser = serial.Serial("/dev/ttyAMA0", 115200)

punctuation = ("Key.space", "Key.enter", "','", "'.'", "'!'", "'?'", "'''", "':'", "';'""'('", "')'", "'-'", "'_'", "'='", "'+'")

punctuation2 = {"Key.space":32, "Key.enter":"10", "','": 44, "'.'": 46, "'!'": 33, "'?'": 63,
  "'''": 39, "':'": 58, "';'": 59, "'('": 40, "')'": 41, "'-'": 45, "'_'": 95, "'='": 61, "'+'": 43,
  "'\"'": 34, "'#'": 35, "'$'": 36, "'%'": 37, "'&'": 38, "'*'": 42, "'/'": 47, "'<'": 60,
   "'>'": 62, "'@'": 64, "'['": 91, "'\\'": 92, "']'": 93, "'^'": 94, "'`'": 96, "'{'": 123, 
   "'|'": 124, "'}'": 125, "'~'": 126}

def write_punct2(key):
    if str(key) in punctuation2.keys():
        code = punctuation2[str(key)]
        ser.write(bytearray([17,code,18,code]))
        ser.flush()
        print("Serial: '{}'".format(chr(code)))

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

    

def autocorrect_to(stri, text):
    if stri != "" and text != (stri[0].lower()+stri[1:]):
        for i in range(0,len(stri)):
            ser.write(bytearray([17,8,18,8]))
            ser.flush()
        if(stri[0].isupper()):
            ser.write(bytearray([17,]))
            ser.write(text[0].encode())
            ser.write(bytearray([18,]))
            ser.write(text[0].encode())
            ser.flush()
            #print("Serial: {}".format(text[0].upper()))
            head = text[0].upper()
        else:
            ser.write(bytearray([17,]))
            ser.write(text[0].upper().encode())
            ser.write(bytearray([18,]))
            ser.write(text[0].upper().encode())
            ser.flush()
            #print("Serial: {}".format(text[0]))
            head = text[0]
        tail = str(text[1:])
        for char in tail:
            ser.write(bytearray([17,]))
            ser.write(char.encode())
            ser.write(bytearray([18,]))
            ser.write(char.encode())
            ser.flush()
        print("Serial: '{}{}'".format(head, tail))
    else:
        print("Serial: leave as '{}'".format(stri))

def on_press(key):
    global stri
    try:
        #print(key)
        #stri += key.char
        if str(key) in punctuation2:
            print("{}".format(stri))
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.sendto(stri.lower().encode(), (host,portAC))
                #text, source = s.recvfrom(1024)
                num, source2 = s.recvfrom(1024)
                #text = text.decode()
                num = int(num.decode())
                #print("suggestion 0: '{}'".format(text))
                print("num: {}".format(repr(num)))
                suggs = []
                text = stri
                for i in range(0, num):
                    sugg, sourcen = s.recvfrom(1024)
                    sugg = sugg.decode()
                    suggs.append(sugg)
                    if i == 0:
                        text = sugg
                    print("Suggestion {}: '{}'".format(i, sugg))
                for i in range(0, num):
                    s.sendto(suggs[i].encode(), (host,portWT))
                    wtype, sourcem = s.recvfrom(1024)
                    wtype = wtype.decode()
                    print("Word Type {}: {}".format(i, wtype))
                autocorrect_to(stri, text)
                write_punct2(key)
                stri = ""
                #print("stri: {}".format(stri))
            stri = ""
            #print("stri: {}".format(stri))
        elif str(key) == "Key.backspace":
            ser.write(bytearray([17,8,18,8]))
            ser.flush()
            stri = stri[:-1]
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
