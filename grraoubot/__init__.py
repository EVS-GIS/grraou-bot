import os
import logging
import yaml

from logging.handlers import TimedRotatingFileHandler

# Set logger
logger = logging.getLogger("grraou-bot")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set console output
console = logging.StreamHandler()
console.setFormatter(formatter)
logger.addHandler(console)

# Read configuration file
grraou_wd = os.path.dirname(os.path.dirname(__file__))

with open(os.path.join(grraou_wd, 'config.yaml')) as f:
    conf = yaml.safe_load(f)
    
# Set logfiles output
logs_dir = os.path.join(grraou_wd, 'logs')
if not os.path.isdir(logs_dir):
    os.mkdir(logs_dir)
    
logfile = TimedRotatingFileHandler(os.path.join(logs_dir, 'grraou-bot.log'), 
                                   when='H', 
                                   interval=conf['app']['logrotate'], 
                                   encoding='UTF-8')
logfile.setFormatter(formatter)
logger.addHandler(logfile)

# Set log level
logger.setLevel(conf['app']['environment'])
logger.info("Configuration loaded")