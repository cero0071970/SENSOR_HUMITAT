# Complete project details at https://RandomNerdTutorials.com

def sub_cb(topic, msg):
  print((topic, msg))
  if topic == b'notification' and msg == b'received':
    print('ESP received hello message')


def connect_and_subscribe(client_id,mqtt_server,topic_sub):
    from umqttsimple import MQTTClient
    #global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server,1883,"kieaCcZaBZZu8vW2cjfn7skwHkLe6SVe0Zcq12psPeLNxxFyEKJB1TVy3xCXdl01","")
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
    return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()





def main():
    from machine import Pin, ADC, SoftI2C
    import ssd1306
    from connexio import do_connect
    import ds1307
    from umqttsimple import MQTTClient
    import time

    from connexio import do_connect
    # CONNECT WIFI
    station2 = do_connect("dlinkosc", "Oscar1970")

    # GPIO PORTS I2C
    I2C_SCL_PORT = 22
    I2C_SDA_PORT = 21
    # GPIO PORT DATA SENSOR
    SENSOR_DATA_PORT = 33
    # MQTT DATA
    mqtt_server = "mqtt.flespi.io"
    client_id = "client_oscar"
    topic_pub = b'humidity1'
    topic_sub = b'humidity1'
    client2=connect_and_subscribe(client_id,mqtt_server, topic_sub)
    client2.publish(topic_pub,b'33',False,0)
    i2c = SoftI2C(scl=Pin(I2C_SCL_PORT), sda=Pin(I2C_SDA_PORT))

    ds = ds1307.DS1307(i2c)
    ds.datetime((2022, 3, 29, 6, 13, 45, 58, 0))
    pp = ds.datetime()
    # ds.datetime()
    oled_width = 128
    oled_height = 64

    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    oled.text("SENSOR HUMITAT", 0, 0)
    oled.text("Created by me!!! :-)", 10, 20)
    oled.text("Xarxa: " + "dlinkosc", 0, 40)
    # oled.text((station2.ifconfig())[0], 0, 50)
    oled.show()
    time.sleep(3)

    POT = ADC(Pin(SENSOR_DATA_PORT))
    POT.atten(ADC.ATTN_11DB)

    oled.text("POTENCIA:", 0, 40)

    oled.show()

    HUM_MAX = 3400
    HUM_MIN = 1400
    min = 4048
    max = 0

    while True:
        HUM_DATA = POT.read()

        # Formula calcul humitat

        HUM = 100 / (HUM_MIN - HUM_MAX) * (HUM_DATA - HUM_MAX)
        if HUM < 0: HUM = 0
        if HUM > 100: HUM = 100
        oled.fill(0)

        # Ens dóna els valors que usarem per HUM_MAX I HUM_MIN
        pp = ds.datetime()
        max = HUM_DATA if max < HUM_DATA else max
        min = HUM_DATA if min > HUM_DATA else min

        oled.text("+SENSOR HUMITAT+", 0, 0)
        oled.text("HUMITAT : " + str(int(HUM)), 10, 23)
        hora = str(pp[2]) + "/" + str(pp[1]) + "/" + (str(pp[0]))[2:4] + " " + str(pp[4]) + ":" + str(
            pp[5]) + ":" + str(pp[6])
        oled.text(hora, 0, 10)
        oled.text("m:" + str(min), 0, 50)
        oled.text("M:" + str(max), 60, 50)
        oled.text("=======================", 0, 40)
        oled.show()
        client2.publish(topic_pub, str(int(HUM)), False, 0)


        time.sleep(0.2)



main()
