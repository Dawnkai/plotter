import logging.config

def setup_logger():
    """
    Start one logger with INFO level on the console and one with DEBUG level
    in file that will be rewritten once it reaches 100kB.
    """
    logging_config = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                # pylint: disable=line-too-long
                'format': "%(asctime)s [%(levelname)-5.5s] [%(module)s] (%(funcName)s) : %(message)s"
            }
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'plotter.log',
                'maxBytes': 100000,
                'backupCount': 1,
                'encoding': 'utf-8',
                'delay': False
            }
        },
        'loggers': {
            '': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True
            }
        }
    }

    logging.config.dictConfig(logging_config)
