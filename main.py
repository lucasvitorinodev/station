import dht
import machine
import time
import urequests
import wifi_library

d=dht.DHT11(machine.Pin(4))
rele = machine.Pin(12, machine.Pin.OUT)

def connect(ssid, password):
    import network
    import time
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    for t in range (50):
        if station.isconnected():
            break
        time.sleep(0.1)
    return station

# Conectando ao wi-fi
print("conectando...")
station = connect("Vitorino" , "12345678")
if not station.isconnected():
    print("Não conectado!")
else:
    print("Conectado!!!")
    
# Iniciar o funcionamento da estacao
while True:
    # Realizar medidas
    d.measure()
    temperature_value = d.temperature()
    humidity_value = d.humidity()
    
    # Exibe medidas de temperatura e umidade
    print("Temperatura = " + str(temperature_value))
    print("Umidade = " + str(humidity_value))
    
    # Verifica se é necessário ligar o rele
    if(humidity_value >= 70 or temperature_value > 31):
        print("Rele ligado!")
        rele.value(1)
    else:
        print("Rele de umidade desligado!")
        rele.value(0)
    
    # Envia a temperatura e umidade para o servidor thing speak 
    updateThingSpeak = "https://api.thingspeak.com/update?api_key=0O4649B4SXI34HVN&field1=" + str(temperature_value) + "&field2=" + str(humidity_value) 
    response = urequests.get(updateThingSpeak)
    print("Update ThingSpeak response: " + response.text)
    print("================================")
    
    time.sleep(30)




