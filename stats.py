import requests
import sys
from bs4 import BeautifulSoup
import settings
import json


help_message = """
Usage: 
    python3 stats.py me
    python3 stats.py group <gid>
"""

class Dartslive:

    def __init__(self):

        # Start a session so we can have persistant cookies
        self.session = requests.session()

    def login(self, username, password):

        session = self.session
        url = 'http://card.dartslive.com/t/doLogin.jsp'
        # This is the form data that the page sends when logging in
        login_data = {
            'i': username,
            'p': password
        }
        r = session.post(url, data=login_data)



    def get_stats(self):
        stats = dict()
        session = self.session
        url = 'http://card.dartslive.com/t/play/index.jsp'
        r = session.get(url)
        bs = BeautifulSoup(r.content)

        item = bs.find('tr', {'class':'statsAvg'})
        avg_01 = item.find('td', {'class':'stats01'}).get_text().split('(')[0].strip()
        avg_cri = item.find('td', {'class':'statsCri'}).get_text().split('(')[0].strip()
        avg_pra = item.find('td', {'class':'statsPra'}).get_text().split('(')[0].strip()
        stats['Avrage'] =  {'01':avg_01, 'Cricket':avg_cri, 'Count Up': avg_pra}

        item = bs.find('tr', {'class':'statsBefore'})
        avg_01 = item.find('td', {'class':'stats01'}).get_text().strip()
        avg_cri = item.find('td', {'class':'statsCri'}).get_text().strip()
        avg_pra = item.find('td', {'class':'statsPra'}).get_text().strip()
        stats['Yesterday'] =  {'01':avg_01, 'Cricket':avg_cri, 'Count Up': avg_pra}

        item = bs.find('tr', {'class':'statsBest'})
        avg_01 = item.find('td', {'class':'stats01'}).get_text().strip()
        avg_cri = item.find('td', {'class':'statsCri'}).get_text().strip()
        avg_pra = item.find('td', {'class':'statsPra'}).get_text().strip()
        stats['Best'] =  {'01':avg_01, 'Cricket':avg_cri, 'Count Up': avg_pra}

        item = bs.find('table', {'id':'award'})
        items = item.find_all('tr')

        stats['Award'] = {}
        for row in items[1:]:
            row = row.get_text().strip().split('\n')
            stats['Award'][row[0]] = row[3]

        return stats

    def get_group_stats(self,gid, stats_type=1):
        session = self.session
        url = 'http://card.dartslive.com/t/group/rank/stats.jsp?type={stats_type}&gid={gid}'
        url = url.format(stats_type=stats_type, gid=gid)
        r = session.get(url)
        bs = BeautifulSoup(r.content)
        items = bs.find_all('li', {'class':'rank'})
        data = []
        for item in items:
            name = item.find('span', {'class':'vsPlayer'}).get_text().strip()
            point = item.find('span', {'class':'point'}).get_text().strip()
            data.append(dict(Name=name, Point=point))
        return data

if __name__ == "__main__":

    dartslive = Dartslive()
    dartslive.login(settings.UID, settings.PIN)
    try:
        if sys.argv[1] == 'me':
            result = dartslive.get_stats()
            print(json.dumps(result, indent=4, sort_keys=True))
        if sys.argv[1] == 'group':
            gid = sys.argv[2]
            result = dartslive.get_group_stats(gid)
            print(json.dumps(result, indent=4, sort_keys=True))
    except:
        print(help_message)



