import time
import pyautogui
import pywhatkit
import requests
import schedule

# API key from NewsAPI
api_key = "..."
# Receiving phone number
p_num = "+..."


def get_news(num_articles):
    # request top headlines from The Netherlands
    main_url = f"https://newsapi.org/v2/top-headlines?country=nl&apiKey={api_key}"
    news = requests.get(main_url).json()
    articles = news["articles"]

    # retrieve article and source from json data
    articles_list = []
    sources_list = []
    for article in articles:
        articles_list.append(str(article["title"]))
        sources_list.append(str(article["url"]))

    # join article and source in list in alternating fashion
    all_items = [None] * (len(articles_list) + len(sources_list))
    all_items[::2] = articles_list
    all_items[1::2] = sources_list

    # format lists in a large string message
    all_items_formatted = "\n".join(all_items[:num_articles * 2])

    return all_items_formatted


def send_message(msg):
    # opens whatsapp web and inputs 'msg' argument in text bar
    # input string number in first argument
    pywhatkit.sendwhatmsg_instantly(str(p_num), msg)

    # search webpage for screenshot of send icon (comment out, only for finding coords of send button)
    coords = pyautogui.locateCenterOnScreen("send.png", grayscale=True, confidence=.8)
    time.sleep(1)

    # click send button
    pyautogui.click(x=1791, y=968)


def activate_bot():
    # send first 5 results of top headlines
    send_message(get_news(5))
    print("News is sent!")


# send message as per schedule
schedule.every(1).minutes.do(activate_bot)

while True:
    schedule.run_pending()
    time.sleep(1)
