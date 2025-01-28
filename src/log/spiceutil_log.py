
import logging

class Log:
    def __init__(self, output_prefix = ''):
        #
        self.m_filename     = f'{output_prefix}.log'
        self.m_logger       = logging.getLogger(self.m_filename)
        self.m_logger.setLevel(logging.INFO)
        #
        stream_handler      = logging.StreamHandler()
        file_handler        = logging.FileHandler(self.m_filename, mode = 'w')
        #
        self.m_logger.addHandler(file_handler)
        self.m_logger.addHandler(stream_handler)
    def GetLogger(self):
        return self.m_logger