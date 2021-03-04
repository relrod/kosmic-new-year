#!/usr/bin/env python

import twitter
import os
import yaml

def setup():
    api = twitter.Api(
        consumer_key=os.environ.get('CONSUMER_KEY'),
        consumer_secret=os.environ.get('CONSUMER_SECRET'),
        access_token_key=os.environ.get('ACCESS_KEY'),
        access_token_secret=os.environ.get('ACCESS_SECRET'))

    # Load in the cached/previously stored tweets
    cache = yaml.safe_load(open('data.yml'))
    latest_id = cache[-1]['id']

    tl = api.GetUserTimeline(
        screen_name='kosmicd12',
        count=200,
        exclude_replies=True,
        include_rts=False,
        since_id=latest_id)

    return (api, cache, latest_id, tl)

def main():
    (api, cache, latest_id, tl) = setup()
    for tweet in tl[::-1]:
        if tweet.quoted_status is not None:
            q = tweet.quoted_status
            if q.id == latest_id:
                new = {
                    'id': tweet.id,
                    'text': tweet.text,
                    'epoch': tweet.created_at_in_seconds,
                }
                print(new)
                cache.append(new)
                latest_id = tweet.id

    with open('data.yml', 'w') as f:
        f.write(yaml.dump(cache))

    out = []
    new_para = False
    for ele in cache[::-1]:
        word = ele['text'].rsplit(' ', 1)[0]
        link = '<a href="https://twitter.com/Kosmicd12/status/{0}">{1}</a>'.format(
            ele['id'],
            word)
        if new_para:
            link = '</p><p>{0}'.format(link)
        new_para = word.endswith('.')
        out.append(link)

    with open('index.html', 'w') as f:
        f.write('''<!doctype html>
<html>
  <head>
    <title>Kosmic's Daily New Year Tweet</title>
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital@0;1&display=swap" rel="stylesheet">
    <style>
      body { margin: 0 auto; width: 600px; }
      p { font-family: 'Playfair Display', serif; font-size: 2em; }
      p.attr { text-align: right; font-size: 1em; }
      p.info { font-size: 0.6em; color: #666; text-align: center; }
      a { text-decoration: none; color: #000; }
    </style>
  </head>
  <body>
    <p>&hellip; %s</p>
    <p class="attr">- <a href="https://twitter.com/Kosmicd12">@Kosmicd12</a></p>
    <p class="info">
      Checks for updates every hour.
      <a href="https://github.com/relrod/kosmic-new-year">open source</a>.
    </p>
  </body>
</html>
''' % ' '.join(out))

if __name__ == '__main__':
    main()
