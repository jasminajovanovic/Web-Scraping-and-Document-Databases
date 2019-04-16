
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

# todo: adsd sleep?
# todo: test / route

url_list = ['https://mars.nasa.gov/news/',
            'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars',
            'https://twitter.com/marswxreport?lang=en',
            'https://space-facts.com/mars/',
            'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars']


def getText(parent):
    return ''.join(parent.find_all(text=True, recursive=False)).strip()


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    browser = init_browser()

    # get latest mars news
    try:
        browser.visit(url_list[0])
        soup = BeautifulSoup(browser.html, "lxml")
        latest_news = soup.find("div", class_="list_text")
        news_title = latest_news.find("div", class_='content_title').text
        news_p = latest_news.find("div", class_='article_teaser_body').text
    except Exception as e:
        print(f"An error occured while scraping {url_list[0]}: {e}")
        news_title = ''
        news_p = ''

    # get featured mars image
    try:
        browser.visit(url_list[1])
        soup = BeautifulSoup(browser.html, "lxml")
        image = soup.find("div", class_="carousel_items")
        relative_img_url = image.article['style'].split(":")[1].split("'")[1]
        featured_img_url = url_list[1].split(
            'spaceimages')[0] + relative_img_url
    except Exception as e:
        print(f"An error occured while scraping {url_list[1]}: {e}")
        featured_img_url = ''

    # get latest mars weather report tweet
    try:
        browser.visit(url_list[2])
        soup = BeautifulSoup(browser.html, "lxml")
        tweets = soup.find_all("div", class_='js-tweet-text-container')
        for tweet in tweets:
            tweet_text = getText(tweet.p)
            if 'InSight sol' in tweet_text:
                mars_weather = tweet_text
    except Exception as e:
        print(f"An error occured while scraping {url_list[2]}: {e}")
        mars_weather = ''

    # get mars facts
    try:
        browser.visit(url_list[3])
        tables = pd.read_html(url_list[3])
        table = tables[0]
        table.columns = ['Parameter', 'Value']
        table.set_index('Parameter')
    except Exception as e:
        print(f"An error occured while scraping {url_list[3]}: {e}")
        table = pd.DataFrame()

    # get images of mars hemishperes, follow image link to obtain full size image
    try:
        browser.visit(url_list[4])
        soup = BeautifulSoup(browser.html, 'lxml')
        items = soup.find_all("div", class_="item")
        base_url = url_list[4].split('search')[0]
        hemisphere_link_urls = []
        for item in items:
            title = item.div.h3.text
            browser.visit(url_list[4])
            browser.click_link_by_partial_text(title)
            soup = BeautifulSoup(browser.html, 'lxml')
            relative_img_url = soup.find("img", class_="wide-image")['src']
            full_img_url = base_url + relative_img_url
            hemisphere_link_urls.append(
                {"title": title, "img_url": full_img_url})
    except Exception as e:
        print(f"An error occured while scraping {url_list[3]}: {e}")
        hemisphere_link_urls = ''

    marsDict = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_img_url': featured_img_url,
        'mars_weather': mars_weather,
        'table': table.to_html(index=False),
        'hemisphere_imgs': hemisphere_link_urls
    }

    browser.quit()
    return marsDict


if __name__ == "__main__":
    marsDict = scrape()
    print(marsDict)
