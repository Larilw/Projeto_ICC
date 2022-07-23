import socketio 

client = socketio.Client()
client.connect("http://192.168.1.16:3000")

aux = True
while(aux):
    x = int(input("Digite x: "))
    y = int(input("Digite y:"))

    client.emit("controle", [x, y])
    if(x == 99):
        break


client.disconnect()