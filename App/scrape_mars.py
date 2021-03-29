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

    ### NASA MARS NEWS

    # Visit Nasa Mars News
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

    ### MARS FACTS

    # Mars Facts: scrape the table containing facts about the planet including Diameter, Mass, etc.
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    html = browser.html

    # Use Pandas to convert the data to a HTML table string
    table = pd.read_html(facts_url)
    mars_facts = table[1]
    # convert table to html
    mars_facts_html = mars_facts.to_html()

    ### MARS HEMISPHERES
    # Mars Hemispheres
    hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hem_url)
    html = browser.html

    # hemisphere urls
    hemisphere_image_urls = [
    "title": "cerberus_enhanced", "img url": "https://astrogeology.usgs.gov/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg",
    "title": "schiaparelli_enhanced", "img url": "https://astrogeology.usgs.gov/cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg",
    "title": "syrtis_major_enhanced", "img url": "https://astrogeology.usgs.gov/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg",
    "title": "valles_marineris_enhanced", "img url": "https://astrogeology.usgs.gov/cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg",
    ] 


    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts_html": mars_facts_html,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
