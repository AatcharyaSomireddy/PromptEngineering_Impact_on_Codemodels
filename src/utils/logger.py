import logging, sys, os

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._build()
        return cls._instance

    def _build(self):
        self.logger = logging.getLogger("benchmark")
        self.logger.setLevel(logging.INFO)
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        self.logger.addHandler(h)

    def get(self):
        return self.logger
