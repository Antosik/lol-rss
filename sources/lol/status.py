from typing import Dict

from sources.base.status import RiotServerStatusCollector


class LOLServerStatusCollector(RiotServerStatusCollector):
    """The class that responsible for collecting server status for League of Legends"""

    def __init__(self, server: Dict[str, str]):
        """Constructor

        Arguments:
            server {Dict[str, str]} -- Server information
        """
        super().__init__('leagueoflegends', 'https://lol.secure.dyn.riotcdn.net/channels/public/x/status/', server)
