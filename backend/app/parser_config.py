from typing import Literal


class ParserConfig:

    def __init__(self):
        self.server = None

    def set_url(self, env: Literal["prod", "dev"]):

        if env == "prod":
            self.server = "http://calcul-kimgerdes.lisn.upsaclay.fr:8002"
        else: 
            self.server = "https://arboratorgrew.elizia.net"