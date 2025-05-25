class Version:
    def __init__(self):
        self.__program = "spiceutil"
        self.__version = "20250601.0.0"

    def get_program(self):
        return self.__program

    def get_version(self):
        return self.__version

    def get_program_version(self):
        return f"{self.get_program()} {self.get_version()}"
