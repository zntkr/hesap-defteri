import logging
import sys
import time
from logging.handlers import RotatingFileHandler

import core.ayarlar as _ayarlar

_FMT = "%(asctime)s.%(msecs)03dZ [%(levelname)s] %(name)s: %(message)s"
_DATE_FMT = "%Y-%m-%dT%H:%M:%S"

logger = logging.getLogger("hesapdefteri")


def setup() -> None:
    """Uygulamanın adlandırılmış logger'ını yapılandırır. main.py'de bir kez çağrılır."""
    if logger.handlers:
        return  # ikinci kez çağrılırsa handler çoğalmaz

    log_dir = _ayarlar.app_dir()
    log_dir.mkdir(parents=True, exist_ok=True)

    handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=1 * 1024 * 1024,  # 1 MB dolunca döner
        backupCount=3,              # app.log, app.log.1, app.log.2, app.log.3
        encoding="utf-8",
    )
    formatter = logging.Formatter(_FMT, datefmt=_DATE_FMT)
    formatter.converter = time.gmtime  # yerel saat değil UTC
    handler.setFormatter(formatter)

    logger.setLevel(logging.WARNING)
    logger.addHandler(handler)
    logger.propagate = False  # root logger'a sızdırmaz


def handle_exception(exc_type: type, exc_value: BaseException, exc_tb) -> None:
    """sys.excepthook olarak atanır; yakalanmamış hataları dosyaya yazar."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_tb)
        return
    logger.critical("Yakalanmamış hata", exc_info=(exc_type, exc_value, exc_tb))
