from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"/Users/d_knowles/Desktop/web-scraping-challenge/App/chromedriver": ChromeDriverManager().install()} (edited) 
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the latest news
    result = soup.find("div", class_='list_text')

    # Extract latest News Title and Paragraph text
    news_title = result.find('a').text
    news_p = result.find('div', class_='article_teaser_body').text

    # Visit the url for JPL Featured Space Image
    image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(image_url)

    # parse html with bs
    html = browser.html
    img_soup = bs(html, "html.parser")

    # find the image url to the full size .jpg image
    results = img_soup.find("div", class_='header')
    full_img = results.find('div', class_='floating_text_area').a['href']

    # save a complete url string for this image
    featured_image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{full_img}'
    
    # BONUS: Find the src for the sloth image
    relative_image_path = soup.find_all('img')[2]["src"]
    sloth_img = url + relative_image_path

    # Store data in a dictionary
    costa_data = {
        "sloth_img": sloth_img,
        "min_temp": min_temp,
        "max_temp": max_temp
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return costa_data
