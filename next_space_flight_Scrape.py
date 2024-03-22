import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

Companies = []
mission_name = []
time = []
location = []

for Page in range (1,226):
    print("we are in page:", Page)
    url = f'https://nextspaceflight.com/launches/past/?page={Page}&search='
    response = requests.get(url)
    response.status_code
    html_content = response.text
    soup = BeautifulSoup(html_content, 'lxml')
    Missions = soup.find_all('div','mdl-cell mdl-cell--6-col')
    for mission in Missions:
        Companies.append(mission.find('div', class_='rcorners a mdl-card__title-text').text.strip())
        mission_name.append(mission.find('h5').text.strip())
        time.append(mission.find('div',class_='mdl-card__supporting-text').text.strip())

launch_sites = [string.split('\n')[-1].split(',')[0].strip() for string in time]
Country = [string.split(',')[-1].strip() for string in time]
locations = [string.split(',')[-2].strip() for string in time]


df = pd.DataFrame({'Company':Companies,'Mission':mission_name,'time':time, 'Launch Site':launch_sites,'location':locations,'Country':Country})
df.to_excel(r"C:\Users\farzaneh\Desktop\Web Scraping\missions.xlsx")
