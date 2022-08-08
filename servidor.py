from inspect import getcallargs
from flask import Flask
from flask_socketio import SocketIO


GPIO_imported = False
try:
    import RPi.GPIO as GPIO
    GPIO_imported = True
except:
    pass

frente_1 = 11
frente_2 = 16
tras_1 = 15
tras_2 = 18

bomba_vcc = 38
bomba_gnd = 40

if(GPIO_imported):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(frente_1, GPIO.OUT)
    GPIO.setup(tras_1, GPIO.OUT)
    GPIO.setup(frente_2, GPIO.OUT)
    GPIO.setup(tras_2, GPIO.OUT)
    GPIO.setup(bomba_vcc, GPIO.IN)
    GPIO.setup(bomba_gnd, GPIO.OUT)


server = Flask(__name__)
socket = SocketIO(server, cors_allowed_origins="*")

def go_esquerda():
    if(GPIO_imported):
        GPIO.output(frente_1, GPIO.HIGH)
        GPIO.output(tras_1, GPIO.LOW)
        GPIO.output(frente_2, GPIO.LOW)
        GPIO.output(tras_2, GPIO.HIGH)

def go_tras():
    if(GPIO_imported):            
        GPIO.output(frente_1, GPIO.HIGH)
        GPIO.output(tras_1, GPIO.LOW)
        GPIO.output(frente_2, GPIO.HIGH)
        GPIO.output(tras_2, GPIO.LOW)

def go_frente():
    if(GPIO_imported):
        GPIO.output(frente_1, GPIO.LOW)
        GPIO.output(tras_1, GPIO.HIGH)
        GPIO.output(frente_2, GPIO.LOW)
        GPIO.output(tras_2, GPIO.HIGH)

def go_direita():
    if(GPIO_imported):
        GPIO.output(frente_1, GPIO.LOW)
        GPIO.output(tras_1, GPIO.HIGH)
        GPIO.output(frente_2, GPIO.HIGH)
        GPIO.output(tras_2, GPIO.LOW)

def parar():
    if(GPIO_imported):
        GPIO.output(frente_1, GPIO.LOW)
        GPIO.output(tras_1, GPIO.LOW)
        GPIO.output(frente_2, GPIO.LOW)
        GPIO.output(tras_2, GPIO.LOW)

@socket.on("connect")
def on_connection():
    print("conectou")

@socket.on("disconnect")
def on_disconnection():
    print("desconectou")

@socket.on("ligarBomba")
def on_bomba_on():
    if(GPIO_imported):
        print("bomba ligada")
        GPIO.setup(bomba_vcc, GPIO.IN)

@socket.on("desligarBomba")
def on_bomba_off():
    if(GPIO_imported):
        print("bomba desligada")
        GPIO.setup(bomba_vcc, GPIO.IN)

@socket.on("controle")
def on_controle(data):
    if((data["x"] < 30 and data["x"] > -30) and (data["y"] < 30 and data["y"] > -30)):
        print("parar")
        parar()
    
    else:
        if(data["x"] > 0):
            if(data["x"] > 50):
                print("dir")
                go_direita()
                
            else:
                if(data["y"] > 50):
                    print("frente")
                    go_frente()
                    
                elif(data["y"] < -50):
                    print("tras")
                    go_tras()
                

        else:
            if(data["x"] < -50):
                print("esquerda")
                go_esquerda()
        
            else:
                if(data["y"] > 50):
                    print("frente")
                    go_frente()


                elif(data["y"] < -50):
                    print("tras")
                    go_tras()
  

if(__name__ == "__main__"):
    try:
        socket.run(server, host="192.168.4.1", port=3000)
    except Exception as e:
        print(str(e))
