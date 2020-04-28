from multiprocessing.dummy import Pool as ThreadPool

class PoolHolder:
    class __TPool:
        def __init__(self, threads):
            self.__threads = threads
            self.__pool = ThreadPool(self.__threads)

        def get_pool(self):
            return self.__pool

        def close(self):
            self.__pool.close()
            self.__pool.join()

    __tpool = None

    @staticmethod
    def instance():
        from flask import current_app
        from githubclient.const import THREADS_ALLOWED

        if PoolHolder.__tpool is None:
            PoolHolder.__tpool = PoolHolder.__TPool(int(current_app.config[THREADS_ALLOWED]))
        return PoolHolder.__tpool
