import logging
import sys
from types import MethodType

# Define custom log levels
VULN_LEVEL_NUM = 60
RUN_LEVEL_NUM = 22
GOOD_LEVEL_NUM = 25

logging.addLevelName(VULN_LEVEL_NUM, 'VULN')
logging.addLevelName(RUN_LEVEL_NUM, 'RUN')
logging.addLevelName(GOOD_LEVEL_NUM, 'GOOD')

# Custom log methods
def _vuln(self, msg, *args, **kwargs):
    if self.isEnabledFor(VULN_LEVEL_NUM):
        self._log(VULN_LEVEL_NUM, msg, args, **kwargs)

def _run(self, msg, *args, **kwargs):
    if self.isEnabledFor(RUN_LEVEL_NUM):
        self._log(RUN_LEVEL_NUM, msg, args, **kwargs)

def _good(self, msg, *args, **kwargs):
    if self.isEnabledFor(GOOD_LEVEL_NUM):
        self._log(GOOD_LEVEL_NUM, msg, args, **kwargs)

logging.Logger.vuln = _vuln
logging.Logger.run = _run
logging.Logger.good = _good

# Custom Formatter and Handler
class CustomFormatter(logging.Formatter):
    def format(self, record):
        msg = super().format(record)
        if record.levelname in log_config.keys():
            msg = '%s %s' % (log_config[record.levelname]['prefix'], msg)
        return msg

class CustomStreamHandler(logging.StreamHandler):
    default_terminator = '\n'

    def emit(self, record):
        if record.msg.endswith('\r'):
            self.terminator = '\r'
            super().emit(record)
            self.terminator = self.default_terminator
        else:
            super().emit(record)

# Log configuration
log_config = {
    'DEBUG': {'value': logging.DEBUG, 'prefix': '[DEBUG]'},
    'INFO': {'value': logging.INFO, 'prefix': '[INFO]'},
    'RUN': {'value': RUN_LEVEL_NUM, 'prefix': '[RUN]'},
    'GOOD': {'value': GOOD_LEVEL_NUM, 'prefix': '[GOOD]'},
    'WARNING': {'value': logging.WARNING, 'prefix': '[WARNING]'},
    'ERROR': {'value': logging.ERROR, 'prefix': '[ERROR]'},
    'CRITICAL': {'value': logging.CRITICAL, 'prefix': '[CRITICAL]'},
    'VULN': {'value': VULN_LEVEL_NUM, 'prefix': '[VULN]'}
}

# Switch logger methods
def _switch_to_no_format_loggers(self):
    self.removeHandler(self.console_handler)
    self.addHandler(self.no_format_console_handler)
    if hasattr(self, 'file_handler') and hasattr(self, 'no_format_file_handler'):
        self.removeHandler(self.file_handler)
        self.addHandler(self.no_format_file_handler)

def _switch_to_default_loggers(self):
    self.removeHandler(self.no_format_console_handler)
    self.addHandler(self.console_handler)
    if hasattr(self, 'file_handler') and hasattr(self, 'no_format_file_handler'):
        self.removeHandler(self.no_format_file_handler)
        self.addHandler(self.file_handler)

# Log utility methods
def _get_level_and_log(self, msg, level):
    if level.upper() in log_config.keys():
        log_method = getattr(self, level.lower())
        log_method(msg)
    else:
        self.info(msg)

def log_red_line(self, amount=60, level='INFO'):
    _switch_to_no_format_loggers(self)
    _get_level_and_log(self, '-' * amount, level)
    _switch_to_default_loggers(self)

def log_no_format(self, msg='', level='INFO'):
    _switch_to_no_format_loggers(self)
    _get_level_and_log(self, msg, level)
    _switch_to_default_loggers(self)

def log_debug_json(self, msg='', data={}):
    if self.isEnabledFor(logging.DEBUG):
        if isinstance(data, dict):
            import json
            try:
                self.debug('{} {}'.format(msg, json.dumps(data, indent=2)))
            except TypeError:
                self.debug('{} {}'.format(msg, data))
        else:
            self.debug('{} {}'.format(msg, data))

# Setup logger
def setup_logger(name='vulnerability_scanner'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    console_handler = CustomStreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(CustomFormatter('%(message)s'))
    logger.addHandler(console_handler)
    
    # Blank handler for no format
    no_format_console_handler = CustomStreamHandler(sys.stdout)
    no_format_console_handler.setLevel(logging.INFO)
    no_format_console_handler.setFormatter(logging.Formatter(fmt=''))
    logger.console_handler = console_handler
    logger.no_format_console_handler = no_format_console_handler
    
    # Methods for custom logging
    logger.red_line = MethodType(log_red_line, logger)
    logger.no_format = MethodType(log_no_format, logger)
    logger.debug_json = MethodType(log_debug_json, logger)
    
    return logger

# Usage example
logger = setup_logger()
logger.info('This is an info message.')
logger.vuln('This is a vulnerability message.')
logger.run('This is a run message.')
logger.good('This is a good message.')
