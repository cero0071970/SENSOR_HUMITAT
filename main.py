def do_connect(SSID, PASSWORD):
    import network  # importa el módulo network
    global station
    station = network.WLAN(network.STA_IF)  # instancia el objeto -station- para controlar la interfaz STA
    station.active(True)
    print(station.scan())
    if not station.isconnected():  # si no existe conexión...
        station.active(True)  # activa el interfaz STA del ESP32
        station.connect(SSID, PASSWORD)  # inicia la conexión con el AP

        print('Conectando a la red', SSID + "...")
        print(station.isconnected())
        while not station.isconnected():  # ...si no se ha establecido la conexión...
            pass  # ...repite el bucle...
    print(station.isconnected())
    print('Configuración de red (IP/netmask/gw/DNS):', station.ifconfig())


def main():
    from machine import Pin, ADC, SoftI2C
    import ssd1306
    import time
    import ds1307
    import umqttsimple
    # GPIO PORTS I2C
    do_connect("dlinkosc", "Oscar1970")  # DESCOMENTAR Y PONER nombre/clave_de_red RED PARA EJECUTAR
    # do_connect("ASUS", "C0nv3rt1d0r33$")  # DESCOMENTAR Y PONER nombre/clave_de_red RED PARA EJECUTAR
    I2C_SCL_PORT = 22
    I2C_SDA_PORT = 21
    # GPIO PORT DATA SENSOR
    SENSOR_DATA_PORT = 33
    SSID = "wlanosc"

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
    oled.text("Xarxa: " + SSID, 0, 40)
    oled.text((station.ifconfig())[0], 0, 50)
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


        oled.show()
        time.sleep(0.01)


main()
