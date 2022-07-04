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

if(GPIO_imported):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(frente_1, GPIO.OUT)
    GPIO.setup(tras_1, GPIO.OUT)
    GPIO.setup(frente_2, GPIO.OUT)
    GPIO.setup(tras_2, GPIO.OUT)
    GPIO.setwarnings(False)


server = Flask(__name__)
socket = SocketIO(server)


@socket.on("connect")
def on_connection():
    print("conectou")

@socket.on("controle")
def on_controle(data):
    print(data)
    if(data[0] == 0):
        if(data[1] == 1):
            print("frente")
            print(GPIO_imported)
            if(GPIO_imported):            
                GPIO.output(frente_1, GPIO.HIGH)
                GPIO.output(tras_1, GPIO.LOW)
                GPIO.output(frente_2, GPIO.HIGH)
                GPIO.output(tras_2, GPIO.LOW)
        elif(data[1] == -1):
            print("tras")
            if(GPIO_imported):
                GPIO.output(frente_1, GPIO.LOW)
                GPIO.output(tras_1, GPIO.HIGH)
                GPIO.output(frente_2, GPIO.LOW)
                GPIO.output(tras_2, GPIO.HIGH)

    elif(data[1] == 0):
        if(data[0] == 1):
            print("direita")
            if(GPIO_imported):
                GPIO.output(frente_1, GPIO.HIGH)
                GPIO.output(tras_1, GPIO.LOW)
                GPIO.output(frente_2, GPIO.LOW)
                GPIO.output(tras_2, GPIO.HIGH)

        elif(data[0] == -1):
            print("esquerda")
            if(GPIO_imported):
                GPIO.output(frente_1, GPIO.LOW)
                GPIO.output(tras_1, GPIO.HIGH)
                GPIO.output(frente_2, GPIO.HIGH)
                GPIO.output(tras_2, GPIO.LOW)

if(__name__ == "__main__"):
    try:
        socket.run(server, host="0.0.0.0", port=3000)
    except Exception as e:
        print(str(e))
