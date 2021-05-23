from bs4 import BeautifulSoup
from requests import get
from environment import gmail, gmail_address
from datetime import datetime
import time

headers = ({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})

base_url = "https://www.oakfurnitureland.co.uk/"

tv_console_url = f"{base_url}/furniture/brooklyn-natural-solid-oak-and-metal-large-tv-unit/1008941.html"
bookcase_url = f"{base_url}/furniture/brooklyn-natural-solid-oak-and-metal-tall-bookcase/1008939.html"
table_chairs_url = f"{base_url}/furniture/brooklyn-living-edge-dining-table-with-2-benches-and-2-chairs/1010037.html"
console_table_url = f"{base_url}/furniture/brooklyn-natural-solid-oak-and-metal-console-table/1008943.html"
bedside_table_url = f"{base_url}/furniture/brooklyn-natural-solid-oak-and-metal-1-drawer-bedside-table/1008933.html"
coffee_table_url = f"{base_url}/furniture/brooklyn-natural-solid-oak-and-metal-coffee-table/1008942.html"
double_bed_url = f"{base_url}/furniture/brooklyn-natural-solid-oak-and-metal-4ft-6-double-bed/1008946.html"
single_bed_url = f"{base_url}/furniture/orrick-rustic-solid-oak-single-bed/5575.html"
chest_of_drawers = f"{base_url}/furniture/brooklyn-natural-solid-oak-and-metal-3-4-chest-of-drawers/1008935.html"

format = "%H:%M:%S"

urls = {"tv_console": tv_console_url,
        "bookcase": bookcase_url,
        "table_chairs": table_chairs_url,
        "console_table": console_table_url,
        "bedside_table": bedside_table_url,
        "coffee_table": coffee_table_url,
        "double_bed": double_bed_url,
        "single_bed": single_bed_url,
        "chest_of_drawers": chest_of_drawers,
        }

price_paid = {"tv_console": 429.99,
              "bookcase": 529.99,
              "table_chairs": 1499.99,
              "console_table": 359.99,
              "bedside_table": 229.99,
              "coffee_table": 339.99,
              "double_bed": 514.99,
              "single_bed": 314.99,
              "chest_of_drawers": 519.99,
              }


def get_prices(urls):
    prices_dict = {}
    for i in urls:

        url = urls.get(i)
        response = get(url, headers=headers)
        html_soup = BeautifulSoup(response.text, 'html.parser')

        if i == "double_bed":
            price = str(html_soup.find('p', attrs={'class': "main-price text-right center"}, recursive=True).find("span"))

        else:
            price = str(html_soup.find('p', attrs={'class': "main-price text-right"}, recursive=True).find("span"))

        price = price.replace("<span>", "")
        price = price.replace("</span>", "")
        price = price.replace("£", "")
        price = price.replace(",", "")
        prices_dict[i] = float(price)

    return prices_dict


def compare_prices(price_paid):
    current_prices = get_prices(urls)
    messages = []
    time_now = datetime.now()

    for i in current_prices:
        if price_paid.get(i) > current_prices.get(i):
            message = f"On {time_now} the current price of {i} is £{current_prices.get(i)} " \
                      f"and you paid £{price_paid.get(i)}. You are owed a refund of " \
                      f"£{price_paid.get(i)-current_prices.get(i)}"
            messages.append(message)

    return messages


def build_mail_message(message_list):
    string = ""
    for message in message_list:
        string = string + f"\n {message}"

    return string


def send_mail(message):
    gmail.send(
        to=gmail_address,
        subject="Changes to Furniture Prices",
        contents=message,
    )


def check_prices_and_send_emails():
    message_list = compare_prices(price_paid)
    message = build_mail_message(message_list)
    send_mail(message)


if __name__ == "__main__":
    while True:
        time_now = datetime.now().time()
        print("The time is:", time_now)

        if datetime.strptime("09:00:00", format).time() < time_now < datetime.strptime("09:01:00", format).time():
            check_prices_and_send_emails()
            print("Sending email...")

        time.sleep(60)  # wait 60 seconds
