import socket

from zeroconf import ServiceInfo, Zeroconf


class SimpleAnnouncer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.zeroconf = Zeroconf()

    def start(self):
        service_info = ServiceInfo(
            "_simple._tcp.local.",
            "SimpleServer._simple._tcp.local.",
            addresses=[socket.inet_aton(self.ip)],
            port=self.port,
        )
        self.zeroconf.register_service(service_info)
        print("Service announced on network. Press Ctrl+C to stop.")

    def stop(self):
        self.zeroconf.close()

if __name__ == "__main__":
    ip = socket.gethostbyname(socket.gethostname())
    port = 12345

    announcer = SimpleAnnouncer(ip, port)
    try:
        announcer.start()
        input("Running... Press Enter to stop.\n")
    except KeyboardInterrupt:
        pass
    finally:
        announcer.stop()
