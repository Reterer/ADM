# server.py
import rpyc
import engine

# import engine
from rpyc.utils.server import ThreadedServer


@rpyc.service
class TestService(rpyc.Service):
    @rpyc.exposed
    def get_home_vac(self, id_user: int, vac_number: int):
        vacs = engine.get_top_n_recommendations(id_user, vac_number)
        print(vacs)
        return [13]


if __name__ == "__main__":
    print("starting server")
    server = ThreadedServer(TestService, port=18811)
    server.start()
