##
import logging


class Singleton(object):
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


##
# Logger Class

class PayNetLogger(Singleton):
    _logger = None

    def initialize(self):
        self._logger = logging.getLogger(__name__)
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler("/tmp/Paynet.app.log", mode="a", encoding="utf-8")
        self._logger.addHandler(console_handler)
        self._logger.addHandler(file_handler)
        formatter = logging.Formatter(
            "{asctime} - {levelname} - {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M",
        )
        console_handler.setFormatter(formatter)

    def sandbox(self):
        if self._logger:
            self._logger.setLevel(logging.INFO)
        else:
            raise ValueError("Logger not created")

    def production(self):
        if self._logger:
            self._logger.setLevel(logging.WARNING)
        else:
            raise ValueError("Logger not created")

    def getLogger(self):
        return self._logger