import scrollphathd as sphd, feedparser as fp, time, datetime, sys, pytz, re
from dotenv import load_dotenv
from loguru import logger
from os import environ

DT_FORMAT_FEED = "%a, %d %b %Y %H:%M:%S %Z"
DT_FORMAT_EP = "%a, %d %b %Y %H:%M:%S %z"
DT_FORMAT_EP_PRINT = "%a, %d %b %Y"


def load_config() -> tuple:
    logger.debug("loading config")

    env_vars = dict(environ)
    podcast_urls = env_vars.get('PODCAST_RSS_URLS', None)
    if not podcast_urls:
        logger.error('could not find podcast urls to parse')
        return {}, True
    
    env = env_vars.get('ENV', 'local')
    log_level = env_vars.get('LOG_LEVEL', 'INFO')
    lookback_hours = int(env_vars.get('LOOKBACK_HOURS', 1)) # TODO add non-int check
    poll_interval = int(env_vars.get('POLL_INTERVAL_MIN', 30)) # TODO add non-int check

    logger.debug("config loaded successfully")
    return {
        'urls': podcast_urls.split(','),
        'env': env,
        'log_level': log_level,
        'lookback': lookback_hours,
        'interval': poll_interval,
    }, False


def parse_datetime(dt: str) -> tuple:
    logger.debug(f"Parsing dt: {dt}")

    if not dt:
        logger.error('dt is empty')
        return (None, True)

    for f in [DT_FORMAT_EP, DT_FORMAT_FEED]:
        try:
            published_dt = datetime.datetime.strptime(dt, f).replace(tzinfo=datetime.timezone.utc)
            return published_dt, False
        except ValueError:
            continue
    
    logger.error(f"Could not parse dt: {dt}")
    return None, True


def parse_ep(ep: dict) -> tuple:
    logger.debug("parsing episode")
    
    title = ep.get('title', 'title not found')
    summary = ep.get('subtitle', None)
    if not summary:
        summary =  re.sub('<[^<]+?>', '', ep.get('summary', ''))
    published_raw = ep.get('published', None)

    published_dt, err = parse_datetime(dt=published_raw)
    if err:
        return {}, True

    logger.debug(f"episode successfully parsed: ({title})")
    return {
        'title': title,
        'summary': summary,
        'published': published_dt
    }, False


def parse_feed(url: str) -> tuple:
    logger.debug(f"parsing feed {url}")

    podcast_feed_rss = fp.parse(url)
    
    podcast_name = podcast_feed_rss.get('feed', {}).get('title', None)
    if not podcast_name:
        logger.error('podcast name not found')
        return {}, True
    
    podcasts = podcast_feed_rss.get('entries', [])
    if len(podcasts) > 0:
        most_recent_ep = podcasts[0]
    else:
        most_recent_ep = None
    
    if not most_recent_ep:
        logger.error('no recent episode found')
        return {}, True
    
    ep_details, err = parse_ep(ep=most_recent_ep)
    if err:
        return {}, True

    logger.debug(f"feed successfully parsed {url}")
    return {
        'name': podcast_name,
        'updated': ep_details.get('published', None),
        'ep': ep_details,
    }, False


def fetch_one(feed_url: str) -> tuple:
    logger.debug(f"fetching {feed_url}")

    podcast_info, err = parse_feed(url=feed_url)
    if err:
        return {}, True

    logger.debug(f"successfully fetched {feed_url}")
    return podcast_info, False


def poll(cfg: dict) -> dict:
    logger.debug("polling")
    
    podcasts_info = {}
    podcast_urls = cfg.get('urls')
    for u in podcast_urls:
        show_details, err = fetch_one(feed_url=u)
        if err:
            continue

        podcast_name = show_details.get('name', 'name not found')
        podcasts_info[podcast_name] = show_details
    
    logger.debug("finished polling")
    return podcasts_info


def display_new_podcast_info(name: str, ep_info: dict, cfg: dict):
    logger.debug("displaying new podcast info")
    env = cfg.get('env')

    ep_publish_dt_formatted = datetime.datetime.strftime(ep_info.get('published'), DT_FORMAT_EP_PRINT)
    
    ep_title = ep_info.get('title')
    ep_summary = ep_info.get('summary')

    logger.info(f"New episode of {name} found")
    logger.info(f"Episode published {ep_publish_dt_formatted}")
    logger.info(f"Episode title: {ep_title}")
    logger.info(f"Episode description: {ep_summary}")

    if env == 'SCROLLPHATHD':
        sphd.clear()
        sphd.set_brightness(0.2)
        
        display_str = f"New episode of {name} published {ep_publish_dt_formatted}. Title: {ep_title}"
        l = sphd.write_string(display_str)
        for _ in range(l):
            sphd.show()
            sphd.scroll(1)
            time.sleep(0.005)
        
        sphd.clear()
        sphd.show()

        time.sleep(10)


def loop(cfg: dict):
    logger.debug('beginning polling loop')
    while True:
        cur_time = datetime.datetime.now().replace(tzinfo=pytz.UTC)
        podcasts_info = poll(cfg=cfg)

        for name, info in podcasts_info.items():
            updated_time = info.get('updated', None)
            if cur_time - datetime.timedelta(hours=cfg['lookback']) < updated_time:
                display_new_podcast_info(name=name, ep_info=info.get('ep'), cfg=cfg)

        logger.debug(f"finished displaying, sleeping for {cfg.get('interval')} minutes...")
        time.sleep(cfg.get("interval") * 60)
    

def main():
    load_dotenv(override=True)
    config, err = load_config()
    if err or not config:
        return
    
    logger.remove()
    logger.add(sys.stderr, level=config.get('log_level'))

    loop(cfg=config)


if __name__ == '__main__':
    main()
