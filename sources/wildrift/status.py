from typing import Any, Dict

from sources.base.status import ServerStatusCollector


class WildRiftServerStatusCollector(ServerStatusCollector):
    """The class that responsible for collecting server status for WildRift"""

    def __init__(self, server: Dict[str, str]):
        super().__init__(server)

    def get_data(self) -> Any:
        return self._request('https://wildrift.secure.dyn.riotcdn.net/channels/public/x/status/{id}.json'.format(id=self.get_server()['id']))

    def construct_alternate_link(self) -> str:
        server = self.get_server()
        return 'https://status.riotgames.com/wildrift?region={region}&locale={locale}'.format(
            region=server['id'],
            locale=server['locale'].replace('-', '_')
        )
