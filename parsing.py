import requests
from bs4 import BeautifulSoup
import fake_useragent
import os.path


def get_data(user_music):
    fakeUser = fake_useragent.UserAgent().random
    headers = {'user-agent': fakeUser}

    url = "https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=en&source=gcsc&gss=.com&cselibv=3e1664f444e6eb06&cx=81ac8cba9f2904c46&q="+ user_music  + "&safe=off&cse_tok=AJvRUv0LrhHhjCAF0McWIZTKQ2MG:1655130776305&lr=&cr=&gl=&filter=0&sort=&as_oq=&as_sitesearch=&exp=csqr,cc&callback=google.search.cse.api16658"
    response = requests.get(url, headers=headers, allow_redirects=True)

    text = list(response.text)

    index_del = next(x for x in range(len(text)) if text[x] == '{')
    del text[0:index_del]

    index_del2 = next(x for x in range(len(text) - 1, -1, -1) if text[x] == '}')
    del text[index_del2 + 1:len(text)]

    with open("f_data.json", "w", encoding="utf-8") as file:
        file.write(''.join(text))


def get_page(name, url):
    fakeUser = fake_useragent.UserAgent().random
    headers = {'user-agent': fakeUser}
    response = requests.get(url, headers=headers, allow_redirects=True)

    with open(f"pages/{name}.html", "w", encoding="utf-8") as file:
        file.write(response.text)


def download_mp3(name, url=""):
    try:
        fakeUser = fake_useragent.UserAgent().random
        headers = {'user-agent': fakeUser}
        response = requests.get(url=url,headers=headers)
        with open(f'music/{name}.mp3', 'wb') as file:
            file.write(response.content)
        return "OK"
    except Exception as e:
        return "fail"


def downloads_music(list):
    for i in list:
        download_mp3(i["Имя песни"].replace('-', ' '), i["Ссылка на mp3"])


def del_music():
    import shutil
    shutil.rmtree("music")


def create_folders():
    if not os.path.exists('music'):
        os.mkdir("music")
    if not os.path.exists('pages'):
        os.mkdir("pages")


def read_data_create_src_music():
    import json
    with open("f_data.json", 'r', encoding="utf-8") as file:
        src = json.load(file)
    list_music = []
    try:
        a = src['results']
    except Exception as e:
        return 0
    for i in src['results']:
        temp = i['unescapedUrl']

        # если ссылка прямая то меняем строку, если нет - скачиваем страницу и парсим еще раз
        if temp.find("music") != -1:
            try:
                temp = i['unescapedUrl'].split('-')

                temp[0] = temp[0][0:len(temp[0]) - 1] + "0"
                temp[1] = "0"
                temp[2] = "1"

                temp = '-'.join(temp) + '-20'
            except Exception as e:
                continue
        else:
            try:
                get_page("temp", i['unescapedUrl'])
                with open("pages/temp.html", encoding="utf-8") as file:
                    page = file.read()
                page = BeautifulSoup(page, 'lxml')
                page_data = page.find('a', class_="loadbtnjs").get("data-file-track")

                temp = "https://muzati.net" + page_data
            except Exception as e:
                if len(list_music):
                    print("Have a problems: download mp3 - " + str(len(list_music)))
                else:
                    print("Мега проблемы")
                continue

        list_music.append({
            "Имя песни": i['richSnippet']['metatags']['ogTitle'],
            "Ссылка на стр": i['unescapedUrl'],
            "Ссылка на mp3": temp
        })
    return list_music

def main_down_music(search):
    del_music()
    print("Удалено")
    create_folders()
    get_data(search)
    print("Страницы скачаны")
    list = read_data_create_src_music()
    if not list:
        print("Ошибка поиска")
        return 1
    else:
        print("Ссылки найдены")
        downloads_music(list)

main_down_music("Привет")

