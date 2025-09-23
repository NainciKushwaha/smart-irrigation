import network
import urequests
from machine import Pin, ADC
import time

# WiFi credentials
ssid = 'Digipodium_4G'
password = 'digipod@123'
# Firebase details
firebase_url ="https://iot-project-768ed-default-rtdb.firebaseio.com/sensor.json"

SOIL_MOISTURE_PIN = 0  # A0 on ESP8266
RELAY_PIN = 5          # D1 on ESP8266

# Crop moisture thresholds (example values)
thresholds = {
    'wheat': 300,
    'rice': 400,
    'corn': 500
}

crop_type = 'wheat'  # Change to your crop

# Connect to WiFi
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(ssid, password)
while not sta_if.isconnected():
    time.sleep(1)

# Setup pins
soil_sensor = ADC(SOIL_MOISTURE_PIN)
relay = Pin(RELAY_PIN, Pin.OUT)
relay.value(0)  # Relay off

while True:
    moisture = soil_sensor.read()
    threshold = thresholds.get(crop_type, 00)
    print('Soil Moisture:', moisture)

    if moisture < threshold:
        relay.value(1)  # Turn on irrigation
        print('Irrigation ON')
    else:
        relay.value(0)  # Turn off irrigation
        print('Irrigation OFF')

    data = {'moisture': moisture}
    response = urequests.put(firebase_url, json=data)
    print(response.text)
    response.close()

    time.sleep(2)