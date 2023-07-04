import requests
from bs4 import BeautifulSoup
from time import sleep
from fake_useragent import UserAgent
import json
ua = UserAgent()

def get_links(text) -> list:
    parsed_data = []
    url = f'https://spb.hh.ru/search/vacancy?text={text}&area=1&area=2&page=0'
    response = requests.get(url, headers={'user-agent':ua.random})
    if response.status_code != 200:
        return
    soup = BeautifulSoup(response.content, 'lxml')
    try:
        page_count = int(soup.find('div',attrs={'class':'pager'}).find_all(
            "span", recursive=False)[-1].find("a").find("span").text)
        print(page_count)
    except:
        return
    for page in range(page_count):
        try:
            url = f'https://spb.hh.ru/search/vacancy?text={text}&area=1&area=2&page={page}'
            response = requests.get(url, headers={'user-agent': ua.random})
            if response.status_code != 200:
                continue
            soup = BeautifulSoup(response.content, 'lxml')
            tags = soup.find_all('div', class_='serp-item')
            for tag in tags:
                links = tag.find('a').get('href').split('?')[0]
                try:
                    if tag.find("span", class_="bloko-header-section-3") == None:
                        continue
                    else:
                        salary_vacancy = tag.find("span", class_="bloko-header-section-3").text
                    company = tag.find('a', class_='bloko-link bloko-link_kind-tertiary').text
                    city = tag.find("div", attrs={"data-qa": "vacancy-serp__vacancy-address"}).text
                    responsed = requests.get(url=links, headers={'user-agent': ua.random})
                    if 'Django' in responsed.text and 'Flask' in responsed.text:
                        parsed_data.append(
                            {
                                "ссылка": links,
                                "зарплата": salary_vacancy,
                                "название компании": company,
                                "город": city
                            })
                except Exception as a:
                    print(f"{a}")
        except Exception as e:
            print(f"{e}")
        sleep(1)
    return parsed_data


if __name__ == "__main__":
    with open('vacancys.json', 'w', encoding='utf-8') as f:
        json.dump(get_links("python"), f, ensure_ascii=False, indent=5)
