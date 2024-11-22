import scrollphathd as sphd, feedparser as fp, requests, time, datetime
from dotenv import load_dotenv
from loguru import logger
from os import environ

DT_FORMAT_FEED = "%a, %d %b %Y %H:%M:%S %Z"
DT_FORMAT_EP = "%a, %d %b %Y %H:%M:%S %z"
load_dotenv()
env_vars = dict(environ)
podcast_urls = dict.get(env_vars, 'PODCAST_RSS_URLS', []).split(',')

def parse_feed(url: str) -> tuple:
    podcast_feed_rss = fp.parse(url)
    updated_time_raw = podcast_feed_rss['updated'] # TODO add err check
   
    try:
        updated_time_dt = datetime.datetime.strptime(updated_time_raw, DT_FORMAT_FEED)
    except ValueError as e:
        logger.error(f"could not parse datetime: {e}")
        return (None, None, True)
    
    podcasts = dict.get(podcast_feed_rss, 'entries', [])
    if len(podcasts) > 0:
        most_recent_ep = podcasts[0]
    else:
        most_recent_ep = None
    
    if not most_recent_ep:
        logger.error('no recent episode found')
        return (None, None, True)
    
    return (updated_time_dt, most_recent_ep, False)


def parse_ep(ep: dict) -> tuple:
    title = dict.get(ep, 'title', 'title not found')
    subtitle = dict.get(ep, 'subtitle', 'subtitle not found')
    published_raw = dict.get(ep, 'published', None)
    if not published_raw:
        logger.error('no published datetime found for episode')
        return (None, True)
    try:
        published_dt = datetime.datetime.strptime(published_raw, DT_FORMAT_EP)
    except ValueError as e:
        logger.error(f"could not parse datetime: {e}")
        return (None, True)

    return ({
        'title': title,
        'subtitle': subtitle,
        'published': published_dt
    }, False)

cur_time = datetime.datetime.now()
for u in podcast_urls:
    update_time_dt, most_recent_ep, err = parse_feed(url=u)
    if err:
        break
    
    ep_details, err = parse_ep(ep=most_recent_ep)
    if err:
        break

    if cur_time - datetime.timedelta(hours=600) < update_time_dt:
        logger.info(f'new episode found: {ep_details["title"]}')


if __name__ == '__main__':
    pass
