"""
def do_connect(SSID, PASSWORD):
    import network  # importa el módulo network
    global station
    station = network.WLAN(network.STA_IF)  # instancia el objeto -station- para controlar la interfaz STA
    if not station.isconnected():  # si no existe conexión...
        station.active(True)  # activa el interfaz STA del ESP32
        station.connect(SSID, PASSWORD)  # inicia la conexión con el AP
        print (station.scan())
        print('Conectando a la red', SSID + "...")

        while not station.isconnected():  # ...si no se ha establecido la conexión...
            pass  # ...repite el bucle...
    print('Configuración de red (IP/netmask/gw/DNS):', station.ifconfig())


do_connect("ASUS", "C0nv3rt1d0r33$")  # DESCOMENTAR Y PONER nombre/clave_de_red RED PARA EJECUTAR
"""