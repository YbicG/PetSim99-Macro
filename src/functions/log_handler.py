import logging
import sys

def init():
    global print
    
    logger_info = logging.getLogger('info_logger')
    logger_info.setLevel(logging.INFO)
    file_handler_info = logging.FileHandler('logfile.log')
    formatter_info = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler_info.setFormatter(formatter_info)
    logger_info.addHandler(file_handler_info)

    logger_error = logging.getLogger('error_logger')
    logger_error.setLevel(logging.ERROR)
    file_handler_error = logging.FileHandler('errors.log')
    formatter_error = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler_error.setFormatter(formatter_error)
    logger_error.addHandler(file_handler_error)

    def log_all_args(*args):
        message = " ".join(str(arg) for arg in args)
        logger_info.info(message)

    original_print = print

    def custom_print(*args, **kwargs):
        log_all_args(*args)
        original_print(*args, **kwargs)
        
    print = custom_print

    def log_exception(exc_type, exc_value, exc_traceback):
        logger_error.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = log_exception
    
    return print
