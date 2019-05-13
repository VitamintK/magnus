import requests
from bs4 import BeautifulSoup
import time
import json
# :authority: autochess.varena.com
# :method: GET
# :path: /api/autochess/player/178236459/matches?limit=20&offset=20&t=1557696019509
# :scheme: https
# accept: application/json, text/plain, */*
# accept-encoding: gzip, deflate, br
# accept-language: en-US,en;q=0.9
# cache-control: no-cache
# cookie: VALang=en_US
# pragma: no-cache
# referer: https://autochess.varena.com/profile/178236459
# user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36

base_url = 'https://autochess.varena.com'


def parse_leaderboard_from_file(html_file: str):
    with open(html_file) as fp:
        soup = BeautifulSoup(fp)
    links = soup.find('section', 'leaderboard-result-list-info').find_all('a')
    #urls = [base_url+link['href'] for link in links]
    profile_ids = [link['href'].split('/')[-1] for link in links]

    # profile_ids = ['40753485']

    s = requests.Session()
    for profile_id in profile_ids:
        print("parsing {}".format(profile_id))
        parse_profile(s, profile_id)
        time.sleep(0.1)

def parse_profile(s, profile_id: str):
    s.headers.update({'referer': base_url + '/profile/' + profile_id})
    # /api/autochess/player/903073770/matches?limit=20&offset=0&t=1557700860245
    matches = []
    offset = 0
    while True:
        unix_time = str(int(time.time()*1000))
        url = '{}/api/autochess/player/{}/matches?limit={}&offset={}&t={}'.format(base_url, profile_id, 20, offset, unix_time)
        r = s.get(url)
        r_json = r.json()
        matches.extend(r_json['data'])
        if len(r_json['data']) < 20:
            break
        offset += len(r_json['data'])
        time.sleep(0.25)
    with open('crawler/raw_data/matches_{}.json'.format(profile_id), 'w') as outfile:
        json.dump(matches, outfile)
    print(len(matches))
# def parse_leaderboard_html(html: str):
#     pass


def main():
    parse_leaderboard_from_file('crawler/leaderboard.html')

if __name__ == '__main__':
    main()
# s = requests.Session()
# s.headers.update({'referer': my_referer})
# s.get(url)