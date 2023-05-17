# server.py
import rpyc
import engine

# import engine
from rpyc.utils.server import ThreadedServer
from functools import lru_cache


@rpyc.service
class TestService(rpyc.Service):
    @rpyc.exposed
    @lru_cache()
    def get_home_vac(self, id_user: int, vac_number: int):
        vacs_ids = engine.get_top_n_recommendations(id_user, vac_number)
        vac_list = engine.get_vacs_by_idx(vacs_ids)
        print(vac_list)
        return vac_list


if __name__ == "__main__":
    print("starting server")
    server = ThreadedServer(TestService, port=18811, hostname="0.0.0.0")
    print(server)
    server.start()
