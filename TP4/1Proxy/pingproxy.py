class PingProxy:

    def __init__(self):
        self.ping = Ping()
        self.pinglibre = PingLibre()

    def execute(self, ip):
        if ip == "192.168.0.254":
            print("Redirigiendo a www.google.com")
            self.pinglibre.executefree("www.google.com")
        else:
            self.ping.execute(ip)