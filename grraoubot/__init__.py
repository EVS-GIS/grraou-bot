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
with open('config.yaml') as f:
    conf = yaml.safe_load(f)
    
# Set logfiles output
if not os.path.isdir('logs'):
    os.mkdir('logs')
    
logfile = TimedRotatingFileHandler('logs/grraou-bot.log', 
                                   when='H', 
                                   interval=conf['app']['logrotate'], 
                                   encoding='UTF-8')
logfile.setFormatter(formatter)
logger.addHandler(logfile)

# Set log level
logger.setLevel(conf['app']['environment'])
logger.info("Configuration loaded")