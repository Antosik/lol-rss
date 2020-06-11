from typing import Dict

from sources.base.status import RiotServerStatusCollector


class LoRServerStatusCollector(RiotServerStatusCollector):
    """Получение данных о статусе сервера"""

    def __init__(self, server: Dict[str, str]):
        """Конструктор класса

        Arguments:
            server {Dict[str, str]} -- Server information
        """
        super().__init__('legendsofruneterra', 'https://bacon.secure.dyn.riotcdn.net/channels/public/x/status/', server)
