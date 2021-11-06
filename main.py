import requests
import os
import telegram
import random
import time

token_telegram_bot = os.environ['TOKEN_BOT']
token_NASA = os.environ['TOKEN_NASA']
bot = telegram.Bot(token=token_telegram_bot)
chat_id = bot.get_updates()[-1].message.chat_id
filename_HST_SM4 = "hubble.jpeg"
url_HST_SM4 = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"
url_spacex = "https://api.spacexdata.com/v4/launches/"
file_path = "images/"
url_NASA = f"https://api.nasa.gov/planetary/apod?api_key={token_NASA}"
url_EPIC = "https://api.nasa.gov/EPIC/api/natural?api_key=DEMO_KEY"


def ensure_dir():
    os.path.exists(file_path)
    os.makedirs(file_path, exist_ok=False)


ensure_dir()


def get_image(url_HST_SM4, file_path, filename_HST_SM4):
    response_HST_SM4 = requests.get(url_HST_SM4)
    response_HST_SM4.raise_for_status()

    with open(f"{file_path} {filename_HST_SM4}", 'wb') as dir:
        dir.write(response_HST_SM4.content)


def fetch_spacex_last_launch(url_spacex, file_path):
    response_spacex = requests.get(url_spacex)
    response_spacex.raise_for_status()
    j = -1

    while True:
        file_path_photoes = response_spacex.json()[j]["links"]["flickr"]["original"]
        if len(file_path_photoes) != 0:
            for i in range(len(file_path_photoes)):
                photo_spacex_url = response_spacex.json()[j]["links"]["flickr"]["original"][i]
                photo_spacex = requests.get(photo_spacex_url)
                with open(f"{file_path} spacex {str(i + 1)} .jpg", 'wb') as dir:
                    dir.write(photo_spacex.content)
            return
        j -= 1


def get_extension_filename(image_NASA):
    return os.path.splitext(image_NASA)


def fetch_NASA_day_launch(url_NASA, file_path):
    response_NASA = requests.get(url_NASA)
    response_NASA.raise_for_status()

    image_NASA = response_NASA.json()["url"]

    expansion = get_extension_filename(image_NASA)[0]
    filename = get_extension_filename(image_NASA)[1]

    response_image_NASA = requests.get(image_NASA)
    response_image_NASA.raise_for_status()

    with open(f"{file_path} {filename} {expansion}", 'wb') as dir:
        dir.write(response_image_NASA.content)


def get_image_EPIC(url_EPIC, token):
    response_EPIC = requests.get(url_EPIC)
    response_EPIC.raise_for_status()
    reponse_EPIC_json = response_EPIC.json()

    for i in range(len(reponse_EPIC_json)):
        image_date_EPIC = reponse_EPIC_json[i]["date"].split()[0]
        image_date_EPIC = image_date_EPIC.split("-", 2)
        image_name_EPIC = reponse_EPIC_json[i]["image"]
        url_image_EPIC = f"https://api.nasa.gov/EPIC/archive/natural/{image_date_EPIC[0]}/{image_date_EPIC[1]}/{image_date_EPIC[2]}/png/{image_name_EPIC}.png?api_key={token}"

        response_image_EPIC = requests.get(url_image_EPIC)
        response_image_EPIC.raise_for_status()

        with open(f"{file_path} planet {str(i + 1)} .png", 'wb') as dir:
            dir.write(response_image_EPIC.content)


def main():
    get_image(url_HST_SM4, file_path, filename_HST_SM4)
    fetch_spacex_last_launch(url_spacex, file_path)
    fetch_NASA_day_launch(url_NASA, file_path)
    get_image_EPIC(url_EPIC, token_NASA)

    while True:
        files = os.listdir(file_path)
        file = files[random.randint(0, len(files) - 1)]
        bot.send_document(chat_id=chat_id, document=open(file_path + file, 'rb'))
        time.sleep(86400)


if __name__ == '__main__':
    main()
