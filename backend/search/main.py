# server.py
import time
import rpyc
from rpyc.utils.server import ThreadedServer


@rpyc.service
class TestService(rpyc.Service):
    @rpyc.exposed
    def get_user(self):
        return time.ctime()

    @rpyc.exposed
    def get_vacs(self):
        return time.ctime()


if __name__ == "__main__":
    print("starting server")
    server = ThreadedServer(TestService, port=18811)
    server.start()
