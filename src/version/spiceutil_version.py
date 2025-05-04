class Version:
    def __init__(self):
        self.m_program = "spiceutil"
        self.m_version = "20250503.0.0"

    def get_program(self):
        return self.m_program

    def get_version(self):
        return self.m_version

    def get_version_summary(self):
        return f"{self.get_program()} {self.get_version()}"
