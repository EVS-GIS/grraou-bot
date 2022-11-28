import requests

from . import logger, conf 
from urllib.parse import urljoin


def mw_login():
    logger.debug('Authenticate to MediaWiki instance')
    session = requests.Session()
    
    # Get a login token
    rep = session.get(conf['mediawiki']['url'], 
                       params={
                           'action': 'query',
                           'meta': 'tokens',
                           'type': 'login',
                           'format': 'json',
                           'formatversion': 2
                       })
    tokens = rep.json()
    logger.debug(tokens)

    # Login
    rep = session.post(conf['mediawiki']['url'], 
                        data={
                            'action': 'login',
                            'lgname': conf['mediawiki']['username'],
                            'lgpassword': conf['mediawiki']['password'],
                            'lgtoken': tokens['query']['tokens']['logintoken'],
                            'format': 'json',
                            'formatversion': 2
                        })
    logger.debug(rep.json())

    return session


def mw_logout(session):
    logger.debug('Logout from MediaWiki instance')
    
    # Get a csrf token
    rep = session.get(conf['mediawiki']['url'], 
                       params={
                           'action': 'query',
                           'meta': 'tokens',
                           'type': 'csrf',
                           'format': 'json',
                           'formatversion': 2
                       })
    tokens = rep.json()
    logger.debug(tokens)
    
    # Logout
    rep = session.post(conf['mediawiki']['url'], 
                       data={
                            'action': 'logout',
                            'token': tokens['query']['tokens']['csrftoken'],
                            'format': 'json',
                            'formatversion': 2
                        })
    logger.debug(f'Response: {rep.status_code}')
    session.close()
    

def get_mw_page():
    logger.debug('Get the content of the MediaWiki Page')

    rep = requests.get(conf['mediawiki']['url'], 
                       params={
                           'action': 'parse',
                           'page': conf['mediawiki']['pagename'],
                           'prop': 'wikitext',
                           'format': 'json',
                           'formatversion': 2
                           })
    
    full_page = rep.json()['parse']['wikitext']
    grraou_start = full_page.find('<!-- GrraouBot content below -->')+32
    mw_data = full_page[:grraou_start]
    
    logger.debug(mw_data)
    
    return mw_data


def generate_table(resources):
    logger.debug("Generate MediaWiki table")
    
    mw_table = '''{| class="wikitable sortable"
|+
!Nom
!Type de ressource'''
    
    for res in resources['resources']:
        mw_table += f'''
|-
|{res['name']}
|{res['typeId']}'''
    
    mw_table += '}'
    logger.debug(mw_table)
    
    return mw_table


def write_mw_page(session, mw_updated_page):
    logger.debug('Write MediaWiki page')
    
    # Get a csrf token
    rep = session.get(conf['mediawiki']['url'], 
                       params={
                           'action': 'query',
                           'meta': 'tokens',
                           'type': 'csrf',
                           'format': 'json',
                           'formatversion': 2
                       })
    tokens = rep.json()
    logger.debug(tokens)
    
    # Edit page
    rep = session.post(conf['mediawiki']['url'],
                       data={
                           'action': 'edit',
                           'title': conf['mediawiki']['pagename'],
                           'bot': 'true',
                           'token': tokens['query']['tokens']['csrftoken'],
                           'text': mw_updated_page,
                           'format': 'json',
                           'formatversion': 2
                       })
    
    logger.debug(rep.json())
    
    if rep.status_code == 200:
        return True
    else:
        return False


def update_page(resources):
    
    mw_data = get_mw_page()
    mw_table = generate_table(resources)
    
    mw_updated_page = mw_data + mw_table
    
    session = mw_login()
    write_mw_page(session, mw_updated_page)
    mw_logout(session)
    
    return
