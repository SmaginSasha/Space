import requests
import os
import telegram
import random
import time

token_telegram_bot = os.environ['TELEGRAM_TOKEN']
token_NASA = os.environ['TOKEN_NASA']
bot = telegram.Bot(token=token_telegram_bot)
chat_id = bot.get_updates()[-1].message.chat_id
file_path = "images/"

os.makedirs(file_path, exist_ok=True)


def get_image(file_path):
    filename_HST_SM4 = "hubble.jpeg"
    url_HST_SM4 = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"

    response_HST_SM4 = requests.get(url_HST_SM4)
    response_HST_SM4.raise_for_status()

    with open(f"{file_path} {filename_HST_SM4}", 'wb') as dir:
        dir.write(response_HST_SM4.content)


def fetch_spacex_last_launch(file_path):
    url_spacex = "https://api.spacexdata.com/v4/launches/"

    response_spacex = requests.get(url_spacex)
    response_spacex.raise_for_status()
    reverse_response_spacex = list(reversed(response_spacex.json()))
    for launch in reverse_response_spacex:
        file_path_photoes = launch["links"]["flickr"]["original"]
        if len(file_path_photoes) != 0:
            for count, url_image_spacex in enumerate(file_path_photoes):
                image_spacex = requests.get(url_image_spacex)
                with open(f"{file_path}spacex{str(count + 1)}.jpg", 'wb') as dir:
                    dir.write(image_spacex.content)
            return


def get_extension_filename(image_NASA):
    return os.path.splitext(image_NASA)


def fetch_NASA_day_launch(file_path, token_NASA):
    payload = {"api_key": f"{token_NASA}", "count": "20", "thumbs": True}
    url_NASA = "https://api.nasa.gov/planetary/apod"

    response_NASA = requests.get(url_NASA, params=payload)
    response_NASA.raise_for_status()

    for count, launch in enumerate(response_NASA.json()):
        image_NASA = launch["url"]
        expansion = get_extension_filename(image_NASA)[1]

        response_image_NASA = requests.get(image_NASA)
        response_image_NASA.raise_for_status()

        with open(f"{file_path}NASA{str(count + 1)}{expansion}", 'wb') as dir:
            dir.write(response_image_NASA.content)


def get_image_EPIC(token):
    payload = {"api_key": "DEMO_KEY"}
    url_EPIC = "https://api.nasa.gov/EPIC/api/natural"

    response_EPIC = requests.get(url_EPIC, params=payload)
    response_EPIC.raise_for_status()
    reponse_EPIC_json = response_EPIC.json()

    for i in range(len(reponse_EPIC_json)):
        image_date_EPIC = reponse_EPIC_json[i]["date"].split()[0]
        image_date_EPIC = image_date_EPIC.split("-", 2)
        image_name_EPIC = reponse_EPIC_json[i]["image"]
        url_image_EPIC = f"https://api.nasa.gov/EPIC/archive/natural/{image_date_EPIC[0]}/{image_date_EPIC[1]}/{image_date_EPIC[2]}/png/{image_name_EPIC}.png?api_key={token}"

        response_image_EPIC = requests.get(url_image_EPIC)
        response_image_EPIC.raise_for_status()

        with open(f"{file_path}planet{str(i + 1)}.png", 'wb') as dir:
            dir.write(response_image_EPIC.content)


def main():
    get_image(file_path)
    fetch_spacex_last_launch(file_path)
    fetch_NASA_day_launch(file_path, token_NASA)
    get_image_EPIC(token_NASA)

    while True:
        files = os.listdir(file_path)
        file = files[random.randint(0, len(files) - 1)]
        bot.send_document(chat_id=chat_id, document=open(file_path + file, 'rb'))
        time.sleep(86400)


if __name__ == '__main__':
    main()
