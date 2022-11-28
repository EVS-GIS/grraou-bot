import requests

from . import logger, conf 
from urllib.parse import urljoin


def lb_authentication():
    # LibreBooking Authentication
    logger.debug("Authentication to LibreBooking API")

    login_url = urljoin(conf['librebooking']['url'], 'Services/index.php/Authentication/Authenticate')
    logger.debug(f"Requesting login URL: {login_url}")
    rep = requests.post(login_url, 
                        json={
                            "username": conf['librebooking']['username'],
                            "password": conf['librebooking']['password']
                            })

    lb_credentials = rep.json()
    logger.debug(lb_credentials)
    
    return lb_credentials
    
    
def lb_logout(lb_credentials):
    # LibreBooking Logout
    logout_url = urljoin(conf['librebooking']['url'], 'Services/index.php/Authentication/SignOut')
    logger.debug(f"Requesting logout URL: {logout_url}")
    rep = requests.post(logout_url,
                        json={
                            "userId": lb_credentials['userId'],
                            "sessionToken": lb_credentials['sessionToken']
                        })
    logger.debug(f"Response: {rep.status_code}")
    
    
def gather_resources(lb_credentials):
    # Gather resources
    logger.debug("Gathering all resources")

    resources_url = urljoin(conf['librebooking']['url'], 'Services/index.php/Resources/')
    logger.debug(f"Requesting URL: {resources_url}")
    rep = requests.get(resources_url,
                    headers={
                        'X-Booked-SessionToken': lb_credentials['sessionToken'],
                        'X-Booked-UserId': lb_credentials['userId']
                    })
    resources = rep.json()
    logger.debug(resources)
    
    return resources


def gather_types(lb_credentials):
    logger.debug("Gathering all resource types")

    resources_url = urljoin(conf['librebooking']['url'], 'Services/index.php/Resources/Groups')
    logger.debug(f"Requesting URL: {resources_url}")
    rep = requests.get(resources_url,
                    headers={
                        'X-Booked-SessionToken': lb_credentials['sessionToken'],
                        'X-Booked-UserId': lb_credentials['userId']
                    })
    resource_types = rep.json()
    logger.debug(resource_types)
    return resource_types


def gather_all():
    lb_credentials = lb_authentication()
    
    resources = gather_resources(lb_credentials)
    # resource_types = gather_types(lb_credentials)
    resource_types = None
    
    lb_logout(lb_credentials)
    
    return resources, resource_types