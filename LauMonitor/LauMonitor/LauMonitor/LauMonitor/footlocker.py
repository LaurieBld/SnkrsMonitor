import requests
from bs4 import BeautifulSoup as soup
import requests
from log import log as log
import time
from datetime import datetime
import random
import sqlite3
from bs4 import BeautifulSoup as soup
from discord_hooks import Webhook
from threading import Thread

class Product():
    def __init__(self, title, link, stock, keyword):
        '''
        (str, str, bool, str) -> None
        Creates an instance of the Product class.
        '''

        # Setup product attributes
        self.title = title
        self.stock = stock
        self.link = link
        self.keyword = keyword


def read_from_txt(path):
    '''
    (None) -> list of str
    Loads up all sites from the sitelist.txt file in the root directory.
    Returns the sites as a list
    '''

    # Initialize variables
    raw_lines = []
    lines = []

    # Load data from the txt file
    try:
        f = open(path, "r")
        raw_lines = f.readlines()
        f.close()

    # Raise an error if the file couldn't be found
    except:
        log('e', "Couldn't locate <" + path + ">.")
        raise FileNotFound()

    if (len(raw_lines) == 0):
        raise NoDataLoaded()

    # Parse the data
    for line in raw_lines:
        lines.append(line.strip("\n"))

    # Return the data
    return lines


def add_to_db(product):
    '''
    (Product) -> bool
    Given a product <product>, the product is added to a database <products.db>
    and whether or not a Discord alert should be sent out is returned. Discord
    alerts are sent out based on whether or not a new product matching
    keywords is found.
    '''

    # Initialize variables
    title = product.title
    stock = str(product.stock)
    link = product.link
    keyword = product.keyword
    alert = False

    # Create database
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS products(title TEXT, link TEXT UNIQUE, stock TEXT, keywords TEXT)""")

    # Add product to database if it's unique
    try:
        c.execute("""INSERT INTO products (title, link, stock, keywords) VALUES (?, ?, ?, ?)""",
                  (title, link, stock, keyword))
        log('s', "Found new product with keyword " + keyword + ". Link = " + link)
        alert = True
    except:
        # Product already exists
        pass
        # log('i', "Product at URL <" + link + "> already exists in the database.")

    # Close connection to the database
    conn.commit()
    c.close()
    conn.close()

    # Return whether or not it's a new product
    return alert


def send_embed(product):
    '''
    (Product) -> None
    Sends a discord alert based on info provided.
    '''

    url = 'https://discordapp.com/api/webhooks/788318805826600972/5oZECMA-AadyUKg2Tr-IH_yQQS8BmvfGG8U_243RzfkOhkA_MGjJqRqrRiTVbbY1YeBb'

    embed = Webhook(url, color=123123)

    embed.set_author(name='LAU')
    embed.set_desc("Produit trouvé !  " + product.keyword)
    embed.add_field(name="Link", value=product.link)

    embed.set_footer(text='LAU',
                     ts=True)

    embed.post()


def monitor(link, keywords):
    '''
    (str, list of str) -> None
    Given a URL <link> and keywords <keywords>, the URL is scanned and alerts
    are sent via Discord when a new product containing a keyword is detected.
    '''

    log('i', "Checking site <" + link + ">...")

    # Parse the site from the link
    pos_https = link.find("https://")
    pos_http = link.find("http://")

    if (pos_https == 0):
        site = link[8:]
        end = site.find("/")
        if (end != -1):
            site = site[:end]
        site = "https://" + site
    else:
        site = link[7:]
        end = site.find("/")
        if (end != -1):
            site = site[:end]
        site = "http://" + site

    # Get all the links on the "New Arrivals" page
    try:
        r = requests.get(link, timeout=5, verify=False)
    except:
        log('e', "Connection to URL <" + link + "> failed. Retrying...")
        time.sleep(5)
        try:
            r = requests.get(link, timeout=8, verify=False)
        except:
            log('e', "Connection to URL <" + link + "> failed.")
            return

    page = soup(r.text, "html.parser")

    raw_links = page.findAll("a")
    hrefs = []

    for raw_link in raw_links:
        try:
            hrefs.append(raw_link["href"])
        except:
            pass

    # Check for links matching keywords
    for href in hrefs:
        found = False
        for keyword in keywords:
            if (keyword.upper() in href.upper()):
                found = True
                if ("http" in href):
                    product_page = href
                else:
                    product_page = site + href
                product = Product("N/A", product_page, True, keyword)
                alert = add_to_db(product)

                if (alert):
                    send_embed(product)


if (__name__ == "__main__"):
    # Ignore insecure messages
    requests.packages.urllib3.disable_warnings()

    # Keywords (seperated by -)
    keywords = [
        "air-force-1-pixel",
        "air-force-1-pixel-summit-white",
        "air-force-1-pixel-gold-chain-summit-white",
        "air-force-1-pixel-gold-chain",
        "air-force-1-pixel-DC1160-100",
        "air-force-1-pixel-blanc",
        "af1-pixel",
        "af1-pixel-gold-chain",
        "af1-pixel-summit-white",
        "blanc-nike-air-force-1-pixel",
        "air-force-one-pixel-summit-white",
        "air-force-one-pixel",
        "air-force-one-gold-chain",
        "air-force-one-gold-chain-summit-white",
        "nike-air-force-one-pixel-femme",
        "nike-air-force-1-pixel-femme",
        "air-force-1-pixel-triple-white",
        "air-force-1-pixel-white-beetroot",
        "air-force-one-pixel-triple-white",
        "air-force-one-pixel-white-beetroot",
        "jordan-1-mid",
        "jordan-one",
        "yeezy-350",
        "yeezy-380",
        "jordan-one",
        "jordan-one-mid",
        "air-max-one",
        "yeezy-700",
        "air-jordan-4",
        "air-jordan-one-mid",
        "air-jordan-one-high",
        "jordan-11-jubilee",
        "air-jordan-one-mid-bred",
        "air-jordan-1-mid-bred",
        "air-jordan-one-low",
        "air-jordan-1-low",
        "dunk-off-white",
        "nike-dunk-rubber-off-white",
        "air-jordan-11-retro",
        "air-jordan-one-mid-se",
        "air-jordan-1-mid-se"
    ]

    # Load sites from file
    sites = read_from_txt("footlocker.txt")

    # Start monitoring sites
    while (True):
        threads = []
        for site in sites:
            t = Thread(target=monitor, args=(site, keywords))
            threads.append(t)
            t.start()
            time.sleep(2)  # 2 second delay before going to the next site
