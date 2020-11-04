from .novelkeys import NovelkeysScraper
from .cannonkeys import CannonkeysScraper
from .konostore import KonostoreScraper
from .tkc import TkcScraper
from .dixiemech import DixieMechScraper
from .txkeyboards import TxKeyboardsScraper

AVAILABLE_SCRAPERS = [
    NovelkeysScraper(),
    CannonkeysScraper(),
    KonostoreScraper(),
    TkcScraper(),
    DixieMechScraper(),
    TxKeyboardsScraper()
]