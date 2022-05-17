import requests
from bs4 import BeautifulSoup
import fake_useragent
import os.path

def get_data(user_music):
    fakeUser = fake_useragent.UserAgent().random
    headers = {'user-agent': fakeUser}

    url = "https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=en&source=gcsc&gss=.com&cselibv=3e1664f444e6eb06&cx=81ac8cba9f2904c46&q=" + user_music + "&safe=off&cse_tok=AJvRUv2HDYaZ_Sm8MdeBFWcXeEab:1652809194976&lr=&cr=&gl=&filter=0&sort=&as_oq=&as_sitesearch=&exp=csqr,cc&callback=google.search.cse.api10204"
    print(url)

    response = requests.get(url, headers=headers, allow_redirects=True)

    text = list(response.text)

    index_del = next(x for x in range(len(text)) if text[x] == '{')
    del text[0:index_del]

    index_del2 = next(x for x in range(len(text) - 1, -1, -1) if text[x] == '}')
    del text[index_del2 + 1:len(text)]

    with open("f_data.json", "w", encoding="utf-8") as file:
        file.write(''.join(text))


def read_data_create_src_music():
    import json
    with open("f_data.json", 'r', encoding="utf-8") as file:
        src = json.load(file)
    list_music = []

    for i in src['results']:
        temp = i['formattedUrl'].split('-')
        temp[0] = temp[0][0:len(temp[0]) - 1] + "0"
        temp[1] = "0"
        temp[2] = "1"

        list_music.append({
            "Имя песни": i['richSnippet']['metatags']['ogTitle'],
            "Ссылка на стр": i['formattedUrl'],
            "Ссылка на mp3": '-'.join(temp) + '-20'
        })
    return list_music


def download_mp3(name, url=""):
    try:
        response = requests.get(url=url)
        with open(f'music/{name}.mp3', 'wb') as file:
            file.write(response.content)
        return "OK"
    except Exception as e:
        return "fail"


def downloads_music(list):

    if not os.path.exists('music'):
        os.mkdir("music")
    for i in list:
        download_mp3(i["Имя песни"].replace('-',' '), i["Ссылка на mp3"])

def del_music():
    import shutil
    shutil.rmtree("music")


def main_down_music(search):
    get_data(search)
    list = read_data_create_src_music()
    downloads_music(list)
