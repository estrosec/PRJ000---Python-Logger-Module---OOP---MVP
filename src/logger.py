from enum import Enum
import inspect, os
from datetime import datetime


class LogLevel(Enum):
    ALL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3

class _LogType(Enum):
    FATAL = 0
    ERROR = 1
    WARNING = 2
    SUCCESS = 3
    INFORMATION = 4
    DEBUG = 5
    TRACE = 6

class Logger:
    def __init__(self, ident: str, toggle_file_logging: bool = False, toggle_db_logging: bool = False):
        self.ident = ident
        self.toggle_file_logging: bool = toggle_file_logging
        self.toggle_db_logging: bool = toggle_db_logging
        self.log_level: LogLevel = LogLevel.ALL
        self.file_path: str = "logs/"
        self.file_logging_timestamp = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
        self.conn = None
        self.cursor = None
        if toggle_db_logging:
            self.__log_db_initialize()

    def __log_db_initialize(self):
        import sqlite3
        self.conn = sqlite3.connect("logs/logs.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                logger TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                header TEXT NOT NULL,
                message TEXT NOT NULL
            )        
        """)

        self.conn.commit()

    def set_log_level(self, log_level: LogLevel):
        self.log_level = log_level

    def set_toggle_file_logging(self, toggle: bool):
        self.toggle_file_logging = toggle

    def set_toggle_db_logging(self, toggle: bool):
        self.toggle_db_logging = toggle
        if toggle:
            self.__log_db_initialize()

    def set_file_path(self, file_path: str):
        self.file_path = file_path

    def fatal(self, message: str):
        if self.log_level.value > LogLevel.LOW.value: return
        self.__log(_LogType.FATAL, message)

    def error(self, message: str):
        if self.log_level.value > LogLevel.LOW.value: return
        self.__log(_LogType.ERROR, message)

    def warning(self, message: str):
        if self.log_level.value > LogLevel.MEDIUM.value: return
        self.__log(_LogType.WARNING, message)

    def success(self, message: str):
        if self.log_level.value > LogLevel.HIGH.value: return
        self.__log(_LogType.SUCCESS, message)

    def information(self, message: str):
        if self.log_level.value > LogLevel.ALL.value: return
        self.__log(_LogType.INFORMATION, message)

    def debug(self, message: str):
        self.__log(_LogType.DEBUG, message)

    def trace(self, message: str):
        frame = inspect.stack()[1]
        filename = frame.filename
        lineno = frame.lineno
        self.__log(_LogType.TRACE, message, filename, lineno)

    def __log(self, log_type: _LogType, message, filename = None, lineno = None):
        header: str = ""
        style_ansi: str = ""

        if log_type == _LogType.FATAL:
            style_ansi = "\033[1m\033[31m"
            header += "[FATAL]:"
        elif log_type == _LogType.ERROR:
            style_ansi = "\033[1m\033[35m"
            header += "[ERROR]:"
        elif log_type == _LogType.WARNING:
            style_ansi = "\033[1m\033[93m"
            header += "[WARNING]:"
        elif log_type == _LogType.SUCCESS:
            style_ansi = "\033[1m\033[32m"
            header += "[SUCCESS]:"
        elif log_type == _LogType.INFORMATION:
            style_ansi = "\033[1m\033[34m"
            header += "[INFORMATION]:"
        elif log_type == _LogType.DEBUG and os.getenv("DEBUG") == "1":
            style_ansi = "\033[2m"
            header += "[DEBUG]:"
        elif log_type == _LogType.TRACE and filename is not None and lineno is not None and os.getenv("DEBUG") == "1":
            style_ansi = "\033[1m\033[90m"
            header += "[TRACE]: - File Path: " + str(filename) + " - Line Number: " + str(lineno) + " -"

        timestamp = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")

        if header != "" and style_ansi != "":
            self.__log_console(timestamp, message, style_ansi, header)
            if self.toggle_file_logging:
                self.__log_file(timestamp, message, header)
            if self.toggle_db_logging:
                self.__log_db(timestamp, message, header)

    def __log_console(self, timestamp, message, style_ansi, header):
            print("\033[96m(" + self.ident + ") \033[0m" + style_ansi + timestamp, "~", header, message + "\033[0m")

    def __log_file(self, timestamp, message, header):
        if os.path.exists(self.file_path):
            try:
                file = open(self.file_path + str(self.file_logging_timestamp).replace("-", "_") + ".log", "a")
                file.write("(" + self.ident +") " + timestamp + " ~ " + header + " " + message + "\n")
                file.close()
            except Exception as e:
                current_toggle_file_logging = self.toggle_file_logging
                self.set_toggle_file_logging(False)
                self.fatal("An error occured... %s" % str(e))
                self.set_toggle_file_logging(current_toggle_file_logging)
        else:
            current_toggle_file_logging = self.toggle_file_logging
            self.set_toggle_file_logging(False)
            self.fatal("File Path for Logger is Not Valid!")
            self.set_toggle_file_logging(current_toggle_file_logging)

    def __log_db(self, timestamp, message, header):
        if self.conn is not None and self.cursor is not None:
            self.cursor.execute("INSERT INTO logs (logger, timestamp, header, message) VALUES (?, ?, ?, ?)", (str(self.ident), str(timestamp), str(header), str(message)))
            self.conn.commit()
