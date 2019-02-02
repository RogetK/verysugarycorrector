from pynput import keyboard
import socket, serial

host = "127.0.0.1"
port = 1235

stri = ""

ser = serial.Serial("/dev/ttyAMA0", 115200)

def on_press(key):
    global stri
    try:
        #print(key)
        #stri += key.char
        if str(key) == 'Key.space':
            print("{}".format(stri))
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.sendto(stri.encode(), (host,port))
                text, source = s.recvfrom(1024)
                num, source2 = s.recvfrom(1024)
                text = text.decode()
                num = int(num.decode())
                print("suggestion 0: '{}'".format(text))
                print("num: {}".format(repr(num)))
                for i in range(0, num-1):
                    sugg = s.recvfrom(1024)
                    #sugg = sugg.decode()
                    #print("Suggestion {}: '{}'".format(i, sugg))
                if text != stri:
                    for i in range(0,len(stri)):
                        ser.write(bytearray([17,8,18,8]))
                        ser.flush()
                    for char in text:
                        ser.write(bytearray([17,]))
                        ser.write(char.encode())
                        ser.write(bytearray([18,]))
                        ser.write(char.encode())
                        ser.flush()
                ser.write(bytearray([17,32,18,32]))
                ser.flush()
                stri = ""
                print("stri: {}".format(stri))
            stri = ""
            print("stri: {}".format(stri))
        elif str(key) == 'Key.backspace':
            ser.write(bytearray([17,8,18,8]))
            ser.flush()
        elif str(key) == 'Key.enter':
            ser.write(bytearray([17,10,18,10]))
            ser.flush()
        else:
            stri += key.char
            print("stri: {}".format(stri))
            ser.write(bytearray([17,]))
            ser.write(key.char.encode())
            ser.write(bytearray([18,]))
            ser.write(key.char.encode())
            ser.flush()
            #pass
            #print('alphanumeric key {0} pressed'.format(key.char))
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
