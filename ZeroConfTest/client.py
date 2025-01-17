from zeroconf import ServiceBrowser, Zeroconf


class SimpleListener:
    def add_service(self, zeroconf, type, name):
        print(f"Service found: {name}")

    def remove_service(self, zeroconf, type, name):
        print(f"Service removed: {name}")

if __name__ == "__main__":
    zeroconf = Zeroconf()
    listener = SimpleListener()
    browser = ServiceBrowser(zeroconf, "_simple._tcp.local.", listener)

    try:
        input("Listening for services... Press Enter to stop.\n")
    except KeyboardInterrupt:
        pass
    finally:
        zeroconf.close()
