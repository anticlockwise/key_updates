USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'


class GroupBuyItem:
    def __init__(self, name, expected_ship_date=None, status=None):
        self._name = name
        self._expected_ship_date = expected_ship_date
        self._status = status

    @property
    def name(self):
        return self._name

    @property
    def expected_ship_date(self):
        return self._expected_ship_date

    @property
    def status(self):
        return self._status

    def __dict__(self):
        return {
            "name": self.name,
            "expected_ship_date": self.expected_ship_date,
            "status": self.status
        }
