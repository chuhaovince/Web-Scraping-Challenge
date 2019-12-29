from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "assets/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    # def variables to store data
    Mars_data = {}

    # find the latest news title and para
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = bs(html, "lxml")
    Mars_data["news_title"] = soup.find("div", class_="content_title").a.text
    Mars_data["news_p"] = soup.find("div", class_="article_teaser_body").text

    # open initial website find full img url
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html,"lxml")

    #get the datalink from this webpage
    md_size = soup.find("footer").a["data-link"] #medium sized
    full_url = "https://www.jpl.nasa.gov" + md_size

    #go to the webpage where the fullsized image can be found
    browser.visit(full_url)
    html = browser.html
    soup = bs(html,"lxml")

    #Get the url for the full-sized image
    lg_size = soup.find("figure").a.img["src"]
    Mars_data['featured_img'] = f"https://www.jpl.nasa.gov{lg_size}"

    # mars weather
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    soup = bs(html,"lxml")
    Mars_data['weather'] = soup.find("p", class_ = "tweet-text").text

    # Mars facts
    url = "https://space-facts.com/mars/"
    df = pd.read_html(url)
    df = df[0]
    Mars_data['table'] = df.to_html()

    # mars hemispheres
    #open main web page
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html,"lxml")
    imgs = soup.find_all("div", class_ = "item") # find all divisions containing differnt hemispheres

    #create an empty dict
    hemispheres = []
    #loop through each hemisophere and get title and image link
    for img in imgs:
        hemisphere = {}
        title = img.find('div', class_="description").a.h3.text
        browser.click_link_by_partial_text(title)
        html = browser.html
        soup = bs(html,"lxml")
        img_link = soup.ul.li.a["href"]
        hemisphere["title"] = title.split(" E")[0]
        hemisphere["img_url"] = img_link
        hemispheres.append(hemisphere)
        browser.back()
    Mars_data['hemispheres'] = hemispheres
    
    # close browser
    browser.quit()

    return Mars_data