import argparse

class ArgParser(argparse.ArgumentParser):
    def __init__(self, exit_on_error=False):
        super().__init__(exit_on_error)

    def error(self, message):
        self.print_usage()
        print(message)
        raise ValueError()