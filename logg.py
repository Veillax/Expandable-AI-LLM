import os
import datetime


class Logger:
    def __init__(self, logfile: str = 'app.log', overwrite: bool = True, pid: str = 'None',
                 debug: bool = False) -> None:
        if os.path.exists(logfile):
            os.remove(logfile)
        self.pid = pid if pid != 'None' else "undefined_process"
        self.logfile = open(logfile, 'w' if overwrite else 'a', encoding='utf-8')
        if debug:
            print('Logger initiated')
        self.debug('logger initiated')

    def log(self, message: str, level: int = 2) -> None:
        try:
            ts = datetime.datetime.today()
            if level == 1:
                lvl = 'DEBUG   '
            elif level == 2:
                lvl = 'INFO    '
            elif level == 3:
                lvl = 'TRACE   '
            elif level == 4:
                lvl = 'EVENT   '
            elif level == 5:
                lvl = 'WARNING '
            elif level == 6:
                lvl = 'ERROR   '
            elif level == 7:
                lvl = 'CRITICAL'
            else:
                lvl = 'LOG     '

            self.logfile.write(str(ts) + " - " + self.pid + " - " + lvl + ": " + message + "\n")
            self.logfile.flush()  # Flush the buffer to ensure immediate write
        except Exception as e:
            print(f"Error while logging: {e}")

    def debug(self, message: str) -> None:
        self.log(message, 1)

    def info(self, message: str) -> None:
        self.log(message, 2)

    def warn(self, message: str) -> None:
        self.log(message, 5)

    def error(self, message: str) -> None:
        self.log(message, 6)

    def critical(self, message: str) -> None:
        self.log(message, 7)

    def other(self, message: str) -> None:
        self.log(message, 0)
