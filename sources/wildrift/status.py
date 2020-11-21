from typing import Any, Dict

from sources.base.status import ServerStatusCollector


class WildRiftServerStatusCollector(ServerStatusCollector):
    """The class that responsible for collecting server status for WildRift"""

    def __init__(self, server: Dict[str, str]):
        """Constructor

        Arguments:
            server {Dict[str, str]} -- Server information
        """
        super().__init__(server)

    def get_data(self) -> Any:
        return self._request('https://wildrift.secure.dyn.riotcdn.net/channels/public/x/status/{id}.json'.format(id=self.get_server()['id']))

    def construct_alternate_link(self) -> str:
        locale = self.get_server()['locale']

        return 'https://status.riotgames.com/wildrift?region={region}&locale={locale}'.format(
            region=locale,
            locale=locale.replace('-', '_')
        )
