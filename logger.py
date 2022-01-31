import logging.config

def setup_logger():
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': "%(asctime)s [%(levelname)-5.5s]  %(message)s"
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
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': 'plotter.log',
                'when': 'D',
                'interval': 1,
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

    logging.config.dictConfig(LOGGING_CONFIG)
