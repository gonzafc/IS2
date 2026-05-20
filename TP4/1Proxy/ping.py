import os

class Ping:

    def execute(self, ip):
        if ip.startswith("192."):
            for i in range(10):
                print(f"Ping {i+1} a {ip}")
        else:
            print("Dirección no permitida")