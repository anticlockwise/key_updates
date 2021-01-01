
import datetime


USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'


class GroupBuyItem:
    def __init__(self, name, store_name, expected_ship_date=None, status=None, update_time=None):
        self._name = name
        self._store_name = store_name
        self._expected_ship_date = expected_ship_date
        self._status = status
        self._update_time = update_time

    @property
    def name(self):
        return self._name

    @property
    def store_name(self):
        return self._store_name

    @property
    def expected_ship_date(self):
        return self._expected_ship_date

    @expected_ship_date.setter
    def expected_ship_date(self, v):
        self._expected_ship_date = v

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, v):
        self._status = v

    @property
    def update_time(self):
        return datetime.datetime.utcnow()

    def __dict__(self):
        return {
            "name": self.name,
            "expected_ship_date": self.expected_ship_date,
            "store_name": self.store_name,
            "status": self.status,
            "update_time": self.update_time
        }
