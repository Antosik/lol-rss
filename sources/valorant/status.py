from typing import Dict

from sources.base.status import RiotServerStatusCollector


class ValorantServerStatusCollector(RiotServerStatusCollector):
    """The class that responsible for collecting server status for Valorant"""

    def __init__(self, server: Dict[str, str]):
        """Contstructor

        Arguments:
            server {Dict[str, str]} -- Server information
        """
        super().__init__('valorant', 'https://valorant.secure.dyn.riotcdn.net/channels/public/x/status/', server)
