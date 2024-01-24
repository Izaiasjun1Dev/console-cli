import logging
from console.config.cli_config import config
import typer

class Application(typer.Typer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(config.logger.level)
        self.logger.propagate = False
        self.logger.handlers = []
        self.logger.addHandler(self.get_console_handler())
        
    def get_console_handler(self):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(config.logger.formater()))
        return console_handler
    
    def run(self):
        self()