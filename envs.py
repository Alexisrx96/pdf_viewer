from os import environ


class EnvVars:
    log_to_console = int(environ.get('LOG_TO_CONSOLE', '0'))
    log_to_file = int(environ.get('LOG_TO_FILE', '0'))
    log_file = environ.get('LOG_FILE', './logs.log')
