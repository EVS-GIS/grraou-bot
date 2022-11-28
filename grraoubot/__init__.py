import logging
import yaml

from logging.handlers import TimedRotatingFileHandler

# Set logger
logger = logging.getLogger("grraou-bot")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console = logging.StreamHandler()
console.setFormatter(formatter)
logger.addHandler(console)

logfile = TimedRotatingFileHandler('logs/grraou-bot.log', when='M', interval=5, encoding='UTF-8')
logfile.setFormatter(formatter)
logger.addHandler(logfile)

# Read configuration file
with open('config.yaml') as f:
    conf = yaml.safe_load(f)

logger.setLevel(conf['app']['environment'])
logger.info("Configuration file loaded")