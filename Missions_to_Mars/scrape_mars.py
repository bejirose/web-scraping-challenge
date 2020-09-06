from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd


def init_browser():
    # Path to the chromedriver
    executable_path = {"executable_path": "C:/Beji/Data Analytics/Downloads/mongo driver/chromedriver_win32/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    print("in scrape_info")
    mars_data = {}
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # find  the latest news
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    news_list = soup.find_all('li', class_='slide')

    # Iterate through each book
    for news in news_list:
        # Use Beautiful Soup's find() method to navigate and retrieve attributes
        news_title = soup.find_all('div', class_='content_title')
        for title in news_title:
            if (title.a):
                latest_news = title.a.text
                print(f'latest News = {latest_news}')
                #rint(latest_news)
                break
        if (news.a):
            latest_text = news.a.text
            #rint(news.a.text)
            break
    #print(f'News Title =\"{latest_news}\"\n')
    #print(f'News Text =\"{latest_text}\"')   

    ## JPL Mars Space Images - Featured Image

    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(jpl_url)

    jpl_html = browser.html

    # Parse HTML with Beautiful Soup
    jpl_soup = bs(jpl_html, 'html.parser')

    featured_image = jpl_soup.find_all('a', class_= 'button fancybox')

    # Iterate through each book
    for tag in featured_image:
        # Use Beautiful Soup's method to find iamge 'href'
        image_url = tag['data-fancybox-href']
        break
    
    complete_url = jpl_url + image_url
    print(f'Featured Image URL = {complete_url}')

    ## Mars Facts

    mars_url = "https://space-facts.com/mars/"

    tables = pd.read_html(mars_url)
    mars_df = tables[0]
    mars_df.rename(columns = {0:'Fact Heading', 1:'Fact Data'}, inplace = True)
    mars_df.set_index('Fact Heading', inplace=True)
    mars_df

    # convert the MARS dataframe to a HTML table string

    mars_html = mars_df.to_html()
    mars_html

    ## Mars Hemispheres

    base_url = "https://astrogeology.usgs.gov/"
    mars_hs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(mars_hs_url)

    mars_hs_html = browser.html

    # Parse HTML with Beautiful Soup
    mars_hs_soup = bs(mars_hs_html, 'html.parser')

    #mars_images = mars_hs_soup.find_all('div', class_='collapsible results')
    mars_images = mars_hs_soup.find_all('div', class_='item')
    #print(mars_images)

    mars_list = []
    # # Iterate through all pages
    for image in mars_images:
        try:
            href = image.a['href']
            title = image.find('img')['alt']
            href = base_url + href
            
            browser.visit(href)
            mars_hs_html = browser.html

            # Parse HTML with Beautiful Soup
            mars_hs_soup = bs(mars_hs_html, 'html.parser')
        
            # wait here for the result to be available before continuing
            # while mars_hs_soup is None:
            #     pass

            mars_image_url = mars_hs_soup.find_all('div', class_='downloads')
            sample = url.a['href']
            for url in mars_image_url:
                #print(mars_image_url.find('h3'))
                #mars_image_url = mars_hs_soup.find_all('div', class_='item')
                sample_url = url.a['href']
                #print(url)
                mars_list.append({'title': title, 'img_url': sample_url})
                break
        except:
            print("scrape complete")
    print(mars_list)



 
    # Store data in a dictionary
    mars_data = {
        "latest_news_title": latest_news,
        "latest_news_text": latest_text,
        "jpl_image": complete_url,
        "mars_fact": mars_html,
        "mars_hemisphere": mars_list
    }

    #print(mars_data)

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
