def importlogdic() -> dict:
    dictConfig: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] - %(module)s :: %(funcName)s() -> %(message)s",
            },
            "error": {
                "format": "[%(asctime)s] - %(module)s :: %(funcName)s() -> %(lineno)s\n %(message)s",
            },
        },
        "handlers": {
            "file": {
                "level": "ERROR",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "FastApiHo.log",
                "formatter": "error",
                "mode": "a",
                "maxBytes": 1048576,
                "encoding": "utf-8",
                "backupCount": 10,
            },
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console", "file"]},
    }
    return dictConfig
