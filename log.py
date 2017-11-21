import logging
import logging.handlers


def create_log(debug, filename):
    # Настройка логов
    lg = logging.getLogger('')
    lg.setLevel(logging.DEBUG)

    # Логи в файл
    fh = logging.handlers.TimedRotatingFileHandler(
        filename + '.log',
        when='W0',
        interval=1,
        backupCount=0,
        encoding=None,
        delay=False,
        utc=False,
        atTime=None)
    formatter = logging.Formatter(fmt='[%(filename)s]%(levelname)-s:%(lineno)d[%(asctime)s]: %(message)s', datefmt=None,
                                  style='%')
    fh.setFormatter(formatter)
    if debug:
        fh.setLevel(logging.DEBUG)
    else:
        fh.setLevel(logging.ERROR)

    # Вывод логов в консоль
    ch = logging.StreamHandler()
    formatter = logging.Formatter(fmt='[%(filename)s]%(levelname)-s:%(lineno)d[%(asctime)s]: %(message)s', datefmt=None,
                                  style='%')
    ch.setFormatter(formatter)
    if debug:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.ERROR)

    # Подклчюение хендлеров
    lg.addHandler(fh)
    lg.addHandler(ch)

    return lg
