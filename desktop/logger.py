import logging
import sys
import os

def setup_logging():
    log_file = 'desktop_app.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger('DesktopApp')
    logger.info("Desktop Application Log Initiated")
    
    return logger

def get_logger(name):
    return logging.getLogger(name)
