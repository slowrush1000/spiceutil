import logging


class Log:
    def __init__(self, output_prefix=""):
        #
        self.m_filename = f"{output_prefix}.log"
        self.m_logger = logging.getLogger(self.m_filename)
        self.m_logger.setLevel(logging.INFO)
        #
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(self.m_filename, mode="w")
        #
        # formatter = logging.Formatter("%(asctime)s %(message)s")
        # stream_handler.setFormatter(formatter)
        # file_handler.setFormatter(formatter)
        #
        self.m_logger.addHandler(file_handler)
        self.m_logger.addHandler(stream_handler)

    def get_logger(self):
        return self.m_logger

    def set_level(self, level):
        if "NOTSET" == level:
            self.set_level_notset()
        elif "DEBUG" == level:
            self.set_level_debug()
        elif "INFO" == level:
            self.set_level_info()
        elif "WARNING" == level:
            self.set_level_warning()
        elif "ERROR" == level:
            self.set_level_error()
        elif "CRITICAL" == level:
            self.set_level_critical()
        else:
            self.set_level_info()

    def set_level_notset(self):
        self.m_logger.setLevel(logging.NOTSET)

    def set_level_debug(self):
        self.m_logger.setLevel(logging.DEBUG)

    def set_level_info(self):
        self.m_logger.setLevel(logging.INFO)

    def set_level_warning(self):
        self.m_logger.setLevel(logging.WARNING)

    def set_level_error(self):
        self.m_logger.setLevel(logging.ERROR)

    def set_level_critical(self):
        self.m_logger.setLevel(logging.ERROR)
