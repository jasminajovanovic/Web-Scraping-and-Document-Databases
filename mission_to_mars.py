

# TODO: error handling - close browser if any errors occur during execution

from splinter import Browser
from bs4 import BeautifulSoup

url_list= ['https://mars.nasa.gov/news/', 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars',          'https://twitter.com/marswxreport?lang=en', 'https://space-facts.com/mars/',         'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars']

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    browser = init_browser()
    browser.visit(url_list[0])
    soup = BeautifulSoup(browser.html)
    latest_news = soup.find("div", class_="list_text")
    news_title = latest_news.find("div", class_='content_title').text
    news_p = latest_news.find("div", class_='article_teaser_body').text


    browser.visit(url_list[1])
    soup = BeautifulSoup(browser.html)
    image = soup.find("div", class_="carousel_items")
    relative_img_url = image.article['style'].split(":")[1].split("'")[1]
    featured_img_url = url_list[1].split('spaceimages')[0] + relative_img_url

    marsDict = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_img_url': featured_img_url
    }

    browser.quit()
    return marsDict

if __name__ == "__main__":
    marsDict = scrape()
    print(marsDict)
