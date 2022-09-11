import requests
from bs4 import BeautifulSoup
import datetime
import pprint
import json

today = datetime.datetime.today()

final_list = []

def politiken():
    url_boghallen = "https://jppol.dk/kalender/?location=boghallen"
    page_boghallen = requests.get(url_boghallen)
    soup = BeautifulSoup(page_boghallen.content, "html.parser")
    results_boghallen = soup.find(class_="main")
    resultset_boghallen = results_boghallen.find_all(class_="teaser teaser--calendar")

    url_forhallen = "https://jppol.dk/kalender/?location=forhallen"
    page_forhallen = requests.get(url_forhallen)
    soup = BeautifulSoup(page_forhallen.content, "html.parser")
    results_forhallen = soup.find(class_="main")
    resultset_forhallen = results_forhallen.find_all(class_="teaser teaser--calendar")

    resultset_consolidated = resultset_boghallen + resultset_forhallen

    for result in resultset_consolidated:
        case = {'venue': result.find(class_="teaser--calendar__cat teaser__cat").text.strip(), 'title': result.find(class_="teaser--calendar__header").text.strip(), 'date': result.find(class_="teaser--calendar__date").text.strip(), 'link': result.find(class_="teaser--calendar__link").get("href")}
        date = case['date'].split('\n')[0].replace(".", "").replace(" ", "-")
        date_format = datetime.datetime.strptime(date, '%d-%b-%Y').strftime('%Y-%m-%d')
        date_format_final = datetime.datetime.strptime(date_format, '%Y-%m-%d')
        time = case['date'].split('—')[-1].replace(" ", "")
        link = case['link']
        title = case['title']
        venue = case['venue']
        case_consolidated = {venue, title, str(date_format_final)[:10], time, link}   
        if date_format_final >= today and date_format_final <= today + datetime.timedelta(days=7):
            final_list.append(case_consolidated)
    print(final_list)
politiken()
