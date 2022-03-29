def main():
    from machine import Pin, ADC, SoftI2C
    import ssd1306
    import time
    import ds1307
    # GPIO PORTS I2C
    I2C_SCL_PORT = 22
    I2C_SDA_PORT = 21
    # GPIO PORT DATA SENSOR
    SENSOR_DATA_PORT = 4

    i2c = SoftI2C(scl=Pin(I2C_SCL_PORT), sda=Pin(I2C_SDA_PORT))

    ds = ds1307.DS1307(i2c)
    ds.datetime((2022, 3, 29, 6,13, 45, 58, 0))
    pp=ds.datetime()
    #ds.datetime()
    oled_width = 128
    oled_height = 64

    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    oled.text("SENSOR HUMITAT", 0, 0)
    oled.text("Created by me!!! :-)", 10, 20)
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
        hora= str(pp[2])+"/"+str(pp[1])+"/"+(str(pp[0]))[2:4]+" "+str(pp[4])+":"+str(pp[5])+":"+str(pp[6])
        oled.text(hora,0,10)
        oled.text("Mimim: " + str(min), 10, 40)
        oled.text("Maxim: " + str(max), 10, 50)

        oled.show()
        time.sleep(0.01)


main()
