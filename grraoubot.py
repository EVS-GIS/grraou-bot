from grraoubot import logger
from grraoubot.librebooking import gather_all
from grraoubot.mediawiki import update_page

# Gather resources from LibreBooking
resources, resource_types = gather_all()
    
# Update MediaWiki page
update_page(resources, resource_types)
