import json
import requests
import time
import config



TOKEN = config.TOKEN
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
API_KEY = config.API_KEY
WEATHER_URL = "https://api.apixu.com/v1/current.json?key={}&q=Paris".format(API_KEY)
HACKER_NEWS_API_KEY = config.HACKER_NEWS_API_KEY
HACKER_NEWS_BASE_URL = 'https://newsapi.org/v2/top-headlines?country=us&apiKey='+HACKER_NEWS_API_KEY


messages = ['Weather info', 'weather', 'weather info']


def get_weather_info(city):
    response = requests.get("https://api.apixu.com/v1/current.json?key={}&q={}".format(API_KEY, city))
    content = response.content.decode("utf8")
    js = json.loads(content)

    data = "Current temperature : {} , Current pressure :  {} , Current wind speed : {},  wind direction : {} , humidity : {}".format(js['current']['temp_c'], js['current']['pressure_mb'], js['current']['wind_mph'], js['current']['wind_dir'], js['current']['humidity'])
    return  data

def get_latest_news_from_hacker_news(i):
    response = requests.get(HACKER_NEWS_BASE_URL)
    content = response.content.decode("utf8")
    js = json.loads(content)
    i = i

    return ( js['articles'][i]['source']['name'], js['articles'][i]['title'], js['articles'][i]['description'],js['articles'][i]['url'], js['articles'][i]['content'])
  




def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    send_message("Here is the weather info of {}".format(text), chat_id)



def echo_all(updates):
    for update in updates["result"]:
        try:
            
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            if text == 'tech news':
                for i in range(10):
                    send_message(get_latest_news_from_hacker_news(i), chat)
            else:
                send_message("Here is the weather info of {}".format(text), chat)
                send_message(get_weather_info(text), chat)

             
        except Exception as e:
            print(e)
    
def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()