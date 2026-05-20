from pingproxy import PingProxy

proxy = PingProxy()

proxy.execute("192.168.0.1")
proxy.execute("192.168.0.254")
proxy.execute("10.0.0.1")