from typing import Dict

from sources.base.status import RiotServerStatusCollector


class LoRServerStatusCollector(RiotServerStatusCollector):
    """The class that responsible for collecting server status for Legends of Runeterra"""

    def __init__(self, server: Dict[str, str]):
        """Contstructor

        Arguments:
            server {Dict[str, str]} -- Server information
        """
        super().__init__('legendsofruneterra', 'https://bacon.secure.dyn.riotcdn.net/channels/public/x/status/', server)
