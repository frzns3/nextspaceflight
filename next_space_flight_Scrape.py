import requests
import pandas as pd
from bs4 import BeautifulSoup
import os


def scrape_and_save_data():
    current_directory = os.getcwd()

    # Create a folder named "output" in the current directory if it doesn't exist
    output_folder = os.path.join(current_directory, 'output')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    Companies = []
    mission_name = []
    time = []
    location = []
    Detail_URL = []
    Group_name = []
    Status = []
    Price = []
    Liftoff = []
    PayLoad_LEO= []
    PayLoad_GTO =[]
    Stage = []
    Strap = []
    Rocket = []
    Fairing = []
    FairingHeight=[]

    base_url = 'https://nextspaceflight.com'

    for Page in range (1, 226):
        print("we are in page:", Page)
        url = f'https://nextspaceflight.com/launches/past/?page={Page}&search='
        response = requests.get(url)
        response.status_code
        html_content = response.text
        soup = BeautifulSoup(html_content, 'lxml')
        Missions = soup.find_all('div', 'mdl-cell mdl-cell--6-col')
        for mission in Missions:
            Companies.append(mission.find('div', class_='rcorners a mdl-card__title-text').text.strip())
            mission_name.append(mission.find('h5').text.strip())
            time.append(mission.find('div', class_='mdl-card__supporting-text').text.strip())

            url_detail = base_url + mission.find('a', class_='mdc-button').get('href')
            Detail_URL.append(url_detail)
            print("The URL is:", url_detail)

            response_detail = requests.get(url_detail)
            response_detail.status_code
            html_content_detail = response_detail.text
            soup_detail = BeautifulSoup(html_content_detail, 'lxml')
            detail_of_missions = soup_detail.find('div', 'page-content')

            Group_name.append(detail_of_missions.find('h4', class_='mdl-card__title-text').text.strip())
            Status.append(detail_of_missions.find('h6', class_='rcorners status').span.text)
            text_ = detail_of_missions.find_all('div', class_="mdl-cell mdl-cell--6-col-desktop mdl-cell--12-col-tablet")

            len_Price = len(Price)
            len_Liftoff = len(Liftoff)
            len_PayLoad_LEO = len(PayLoad_LEO)
            len_PayLoad_GTO = len(PayLoad_GTO)
            len_Stage = len(Stage)
            len_Strap = len(Strap)
            len_Rocket = len(Rocket)
            len_Fairing = len(Fairing)
            len_FairingHeight = len(FairingHeight)

            for element in text_:
                text = element.text.strip()
                if "Price:" in text:
                    Price.append(text.split(': ')[1])
                elif "Liftoff Thrust:" in text:
                    Liftoff.append(text.split(': ')[1])
                elif "Payload to LEO:" in text:
                    PayLoad_LEO.append(text.split(': ')[1])
                elif "Payload to GTO:" in text:
                    PayLoad_GTO.append(text.split(': ')[1])
                elif "Stages:" in text:
                    Stage.append(text.split(': ')[1])
                elif "Strap-ons:" in text:
                    Strap.append(text.split(': ')[1])
                elif "Rocket Height:" in text:
                    Rocket.append(text.split(': ')[1])
                elif "Fairing Diameter:" in text:
                    Fairing.append(text.split(': ')[1])
                elif "Fairing Height:" in text:
                    FairingHeight.append(text.split(': ')[1])

            if len(Price) == len_Price:
                Price.append(None)

            if len(Liftoff) == len_Liftoff:
                Liftoff.append(None)

            if len(PayLoad_LEO) == len_PayLoad_LEO:
                PayLoad_LEO.append(None)

            if len(PayLoad_GTO) == len_PayLoad_GTO:
                PayLoad_GTO.append(None)

            if len(Stage) == len_Stage:
                Stage.append(None)

            if len(Strap) == len_Strap:
                Strap.append(None)

            if len(Rocket) == len_Rocket:
                Rocket.append(None)

            if len(Fairing) == len_Fairing:
                Fairing.append(None)

            if len(FairingHeight) == len_FairingHeight:
                FairingHeight.append(None)

    launch_sites = [string.split('\n')[-1].split(',')[0].strip() for string in time]
    Country = [string.split(',')[-1].strip() for string in time]
    locations = [string.split(',')[-2].strip() for string in time]

    df = pd.DataFrame({'Company':Companies,'Mission':mission_name,'time':time, 'Launch Site':launch_sites,
                       'location':locations,'Country':Country,'Detail Link':Detail_URL,'Group_Name':Group_name,'Status':Status,
                       'Price':Price,"Liftoff":Liftoff,"PayLoad_LEO":PayLoad_LEO,"PayLoad_GTO":PayLoad_GTO,
                       "Stage":Stage,"Strap":Strap,"Rocket_Height":Rocket,"Fairing_diameter":Fairing,"FairingHeight":FairingHeight
                       })

    # Define the file name
    file_name = 'missions.xlsx'

    # Construct the full file path
    file_path = os.path.join(output_folder, file_name)

    # Save the DataFrame to Excel using the constructed file path
    df.to_excel(file_path)

    print("File saved successfully at:", file_path)

# Call the function to execute the scraping and saving process
scrape_and_save_data()
