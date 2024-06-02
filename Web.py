import requests
from bs4 import BeautifulSoup
import csv

date = input("Enter a date in the following format MM/DD/YY: ")
page = requests.get(f"https://www.yallakora.com/match-center?date={date}")


def main(page):
    src = page.content
    soup = BeautifulSoup(src, "lxml")
    matches_details = []

    championships = soup.find_all("div", {'class': 'matchCard'})

    def get_match_info(championships):
        championship_title = championships.contents[1].find('h2').text.strip()
        all_matches = championships.contents[3].find_all('li')
        number_of_matches = len(all_matches)

        for i in range(number_of_matches):
            team_A = all_matches[i].find(
                'div', {'class': 'teamA'}).text.strip()
            team_B = all_matches[i].find(
                'div', {'class': 'teamB'}).text.strip()
            match_result = all_matches[i].find(
                'div', {'class': 'MResult'}).find_all('span', {'class': 'score'})
            score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"
            match_time = all_matches[i].find('div', {'class': 'MResult'}).find(
                'span', {'class': 'time'}).text.strip()
            matches_details.append({"الدوري": championship_title, "الفريق الاول": team_A, "الفريق الثاني": team_B,
                                    "موعد المباراة": match_time, "نتيجة المباراة": score})

    for i in range(len(championships)):
        get_match_info(championships[i])

    keys = matches_details[0].keys()
    file_name = input("Enter the name of csv file : ")
    with open(fr'D:\Abdo ElDeeb\Web Scraping\Yala Cora\CSV file\{file_name}.csv', 'w', newline='', encoding='utf-8-sig') as output_file:
        dic_writer = csv.DictWriter(output_file, keys)
        dic_writer.writeheader()
        dic_writer.writerows(matches_details)
        print("File created")


main(page)
