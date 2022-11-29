import argparse

class Settings:
    """
    Options and settings for crossfit.py
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument(
            "-u", "--user", default="ollehman", help="username for user account"
        )
        self.parser.add_argument(
            "-p", "--password", default=None, help="password for user account"
        )
        self.parser.add_argument(
            "-nr", "--lessonNr", nargs="+", help="lesson number to sign up for."
        )
        self.parser.add_argument(
            "-d", "--debug", action="store_true", 
            help="whether to run in debug mode or not. This will show the browser if set to True."
        )
        self.parser.add_argument(
            "-f", "--friend", action="store_true", 
            help="whether to run in friend mode or not. This will only notify and not signup."
        )


    def parse(self):
        self.settings = self.parser.parse_args()
        return self.settings
