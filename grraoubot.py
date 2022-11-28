from grraoubot import logger
from grraoubot.librebooking import gather_all
from grraoubot.mediawiki import update_page

# Gather resources from LibreBooking
try:
    resources, resource_types = gather_all()
except:
    logger.error('There was an error gathering LibreBooking resources. Please check the logs')
    
try:
    # Update MediaWiki page
    update_page(resources)
except:
    logger.error('There was an error updating the MediaWiki page. Please check the logs')
