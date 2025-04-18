import argparse

class CommonArgs:

    def __init__(self, prog: str, args=None):
        parser = argparse.ArgumentParser(prog)
        parser.add_argument("work_dir", help="working directory")
        parser.add_argument("config_file", help="yaml config file")
        self._parsed_args = vars(parser.parse_args(args))

    def get_parsed_arguments(self):
        return self._parsed_args

    def get_work_dir(self):
        return self._parsed_args["work_dir"]

    def get_config_file(self):
        return self._parsed_args["config_file"]
