import logging


class Log:
    def __init__(self, output_prefix=""):
        #
        self.__file_name = f"{output_prefix}.log"
        self.__logger = logging.getLogger(self.__file_name)
        self.__logger.setLevel(logging.INFO)
        #
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(self.__file_name, mode="w")
        #
        # formatter = logging.Formatter("%(asctime)s %(message)s")
        # stream_handler.setFormatter(formatter)
        # file_handler.setFormatter(formatter)
        #
        self.__logger.addHandler(file_handler)
        self.__logger.addHandler(stream_handler)

    def get_logger(self):
        return self.__logger

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
        self.__logger.setLevel(logging.NOTSET)

    def set_level_debug(self):
        self.__logger.setLevel(logging.DEBUG)

    def set_level_info(self):
        self.__logger.setLevel(logging.INFO)

    def set_level_warning(self):
        self.__logger.setLevel(logging.WARNING)

    def set_level_error(self):
        self.__logger.setLevel(logging.ERROR)

    def set_level_critical(self):
        self.__logger.setLevel(logging.ERROR)

    def get_file_name(self):
        return self.__file_name
