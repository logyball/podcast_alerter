# Description

A physical reminder when a new podcast shows up.  Uses RSS feeds and a Raspberry PI Screen to display the reminders.

## Requirements

#### Locally
- `python3`

#### With PiHat
- Raspberry PI compatible with PI HAT [ScrollPhatHD PI HAT](https://shop.pimoroni.com/en-us/products/scroll-phat-hd).  I went with the Zero W
- `python3`
- [ScrollPhatHD PI HAT](https://shop.pimoroni.com/en-us/products/scroll-phat-hd) (obviously)
- Compatible Raspberry PI with I2C connection enabled, and [PI HAT installed](https://learn.pimoroni.com/article/getting-started-with-scroll-phat-hd)
- On your Raspberry PI: `sudo apt-get install python3-numpy python3-virtualenv`


## Setup

- `python -m virtualenv venv`
- `source ./venv/bin/activate`
- `pip install -r requirements.txt`

### Configuration

Configuration is done in a local `.env`.  Copy the `.env.example` to a file called `.env` in the same directory and configure these variables:

- `PODCAST_RSS_URLS`: Set to a comma-delimited list of podcast RSS feeds
- `ENV`: set to 'local' to work on your machine, set to 'SCROLLPHATHD' to display on your PI
- `LOOKBACK_HOURS`: set to the number of hours before now you'd like an episode to be considered "new"
- `POLL_INTERVAL_MIN`: how often to check for new podcasts in minutes
- `LOG_LEVEL`: logging level

## Running

```sh

# in your virtual environment, simply run python main.py

> python main.py

2024-11-22 16:09:06.739 | DEBUG    | __main__:load_config:12 - loading config
2024-11-22 16:09:06.739 | DEBUG    | __main__:load_config:25 - config loaded successfully
2024-11-22 16:09:06.741 | DEBUG    | __main__:loop:149 - beginning polling loop
2024-11-22 16:09:06.741 | DEBUG    | __main__:poll:102 - polling
2024-11-22 16:09:06.741 | DEBUG    | __main__:fetch_one:91 - fetching https://citationsneeded.libsyn.com/rss
2024-11-22 16:09:06.741 | DEBUG    | __main__:parse_feed:59 - parsing feed https://citationsneeded.libsyn.com/rss
2024-11-22 16:09:07.371 | DEBUG    | __main__:parse_ep:36 - parsing episode
2024-11-22 16:09:07.372 | DEBUG    | __main__:parse_ep:50 - episode successfully parsed: (Episode 212: Gaza and the Political Utility of Selective Empathy)
2024-11-22 16:09:07.372 | DEBUG    | __main__:parse_feed:82 - feed successfully parsed https://citationsneeded.libsyn.com/rss
2024-11-22 16:09:07.373 | DEBUG    | __main__:fetch_one:97 - successfully fetched https://citationsneeded.libsyn.com/rss
2024-11-22 16:09:07.373 | DEBUG    | __main__:fetch_one:91 - fetching https://podcast.darknetdiaries.com/
2024-11-22 16:09:07.373 | DEBUG    | __main__:parse_feed:59 - parsing feed https://podcast.darknetdiaries.com/
2024-11-22 16:09:07.713 | DEBUG    | __main__:parse_ep:36 - parsing episode
2024-11-22 16:09:07.713 | DEBUG    | __main__:parse_ep:50 - episode successfully parsed: (151: Chris Rock)
2024-11-22 16:09:07.714 | DEBUG    | __main__:parse_feed:82 - feed successfully parsed https://podcast.darknetdiaries.com/
2024-11-22 16:09:07.714 | DEBUG    | __main__:fetch_one:97 - successfully fetched https://podcast.darknetdiaries.com/
2024-11-22 16:09:07.714 | DEBUG    | __main__:fetch_one:91 - fetching https://feeds.soundcloud.com/users/soundcloud:users:211911700/sounds.rss
2024-11-22 16:09:07.714 | DEBUG    | __main__:parse_feed:59 - parsing feed https://feeds.soundcloud.com/users/soundcloud:users:211911700/sounds.rss
2024-11-22 16:09:09.137 | DEBUG    | __main__:parse_ep:36 - parsing episode
2024-11-22 16:09:09.137 | DEBUG    | __main__:parse_ep:50 - episode successfully parsed: (886 - Cabinet Curiosity feat. Alex Nichols (11/18/24))
2024-11-22 16:09:09.138 | DEBUG    | __main__:parse_feed:82 - feed successfully parsed https://feeds.soundcloud.com/users/soundcloud:users:211911700/sounds.rss
2024-11-22 16:09:09.138 | DEBUG    | __main__:fetch_one:97 - successfully fetched https://feeds.soundcloud.com/users/soundcloud:users:211911700/sounds.rss
2024-11-22 16:09:09.138 | DEBUG    | __main__:poll:114 - finished polling
2024-11-22 16:09:09.138 | DEBUG    | __main__:display_new_podcast_info:119 - displaying new podcast info
2024-11-22 16:09:09.138 | INFO     | __main__:display_new_podcast_info:126 - New episode of Citations Needed found
2024-11-22 16:09:09.138 | INFO     | __main__:display_new_podcast_info:127 - Episode published Wed, 20 Nov 2024
2024-11-22 16:09:09.138 | INFO     | __main__:display_new_podcast_info:128 - Episode title: Episode 212: Gaza and the Political Utility of Selective Empathy
2024-11-22 16:09:09.138 | INFO     | __main__:display_new_podcast_info:129 - Episode description: "Salvadoran Ties Bloodshed To a 'Culture of Violence'", reported The New York Times in 1981. "The violence in Lebanon is casual, random, and probably addicting," stated the Honolulu Star-Advertiser in 1985. "Muslim life is cheap, most...
2024-11-22 16:09:09.139 | DEBUG    | __main__:display_new_podcast_info:119 - displaying new podcast info
2024-11-22 16:09:09.139 | INFO     | __main__:display_new_podcast_info:126 - New episode of Darknet Diaries found
2024-11-22 16:09:09.139 | INFO     | __main__:display_new_podcast_info:127 - Episode published Tue, 05 Nov 2024
2024-11-22 16:09:09.139 | INFO     | __main__:display_new_podcast_info:128 - Episode title: 151: Chris Rock
2024-11-22 16:09:09.139 | INFO     | __main__:display_new_podcast_info:129 - Episode description: Chris Rock
2024-11-22 16:09:09.139 | DEBUG    | __main__:display_new_podcast_info:119 - displaying new podcast info
2024-11-22 16:09:09.139 | INFO     | __main__:display_new_podcast_info:126 - New episode of Chapo Trap House found
2024-11-22 16:09:09.139 | INFO     | __main__:display_new_podcast_info:127 - Episode published Tue, 19 Nov 2024
2024-11-22 16:09:09.139 | INFO     | __main__:display_new_podcast_info:128 - Episode title: 886 - Cabinet Curiosity feat. Alex Nichols (11/18/24)
2024-11-22 16:09:09.139 | INFO     | __main__:display_new_podcast_info:129 - Episode description: We review the various freaks, toadies, goons, and…
2024-11-22 16:09:09.139 | DEBUG    | __main__:loop:159 - finished displaying, sleeping for 1 minutes...
```

## How do I find a Podcast's RSS feed?

I used https://castos.com/tools/find-podcast-rss-feed/

## Future Work

So far I've tested this with `libsyn.com`, `soundcloud.com`, `substack`, and other podcasts' custom RSS feeds.  Hopefully it's generic enough for all the possible permutations!
