def do_connect(SSID, PASSWORD):
    import network  # importa el módulo network

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
    return (station)

