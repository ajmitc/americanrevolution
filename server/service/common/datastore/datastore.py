import os

class DataStore:
    DATABASE_INSTALL_DIR = "database/install/"

    def __init__(self):
        pass

    def connect(self):
        pass

    def query(self, statement, values=None):
        pass

    def execute(self, statement, values=None):
        pass

    def close(self):
        pass

    def install(self, filepath):
        pass

    def run_install(self, version):
        for root, dirs, files in os.walk(os.path.join(self.DATABASE_INSTALL_DIR, version)):
            for file in files:
                if file.endswith(".sql"):
                    self.install(os.path.join(root, file))
