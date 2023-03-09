import logging

import ecs_logging

from configs.Config import Config

config = Config()


class LoggingFile:

    def get_logger(self, class_name):
        logger = logging.getLogger(class_name)
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(config.get_txt_output_path())
        handler.setFormatter(ecs_logging.StdlibFormatter())
        logger.addHandler(handler)
        return logger
