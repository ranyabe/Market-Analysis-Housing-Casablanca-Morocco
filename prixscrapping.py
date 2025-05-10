

from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import numpy as np
import pandas as pd



def on_listings_page(browser):
    '''
    Check if the browser is on a page with property listings on the mubawab website
    
    params
        browser: the selenium webdriver used to make requests
    '''
    try:
        browser.find_element_by_xpath('/html/body/section/div[2]/div[1]/div[2]/i')
        return True
    except NoSuchElementException:
        return False

def get_listing(browser,ard,qrt=None,n=0):
    '''
    This function gets the info of the n'th listing on a listings page and goes back to that page
    
    params
        browser: the selenium webdriver used to make requests
        ard: the district selected to land on listings page
        qrt: if it was used, the neighbourhood selected to land on listings page, otherwise None
    '''
    listing = browser.find_element_by_xpath(f"//li[@class='listingBox w100'][{n+1}]")
    listing.click()
    try:
        type_ = browser.find_element_by_xpath('/html/body/section/div[1]/div/div[1]/a[3]').text
    except:
        type_ = np.nan
    try:
        title = browser.find_element_by_xpath('/html/body/section/div[2]/div/div[1]/h1').text
    except:
        title = np.nan
    try:
        loca = browser.find_element_by_xpath('/html/body/section/div[2]/div/div[1]/h3').text
    except:
        loca = np.nan
    try:
        map_click = browser.find_element_by_xpath('/html/body/section/div[2]/div/div[8]/div[1]/div/a')
        map_click.click()
        coord = browser.find_element_by_xpath('/html/body/section/div[2]/div/div[8]/div[2]')
        lat = coord.get_attribute("lat")
        lon = coord.get_attribute("lon")
    except:
        lat = np.nan
        lon = np.nan
    try:
        price = browser.find_element_by_xpath('/html/body/section/div[2]/div/div[1]/div[1]/div[1]/h3').text
    except:
        price = np.nan
    try:
        tags = browser.find_elements_by_xpath('/html/body/section/div[2]/div/div[1]/div[2]/span')
    except:
        tags = np.nan
    try:
        other_tags = [tag.text for tag in tags]
    except:
        other_tags = np.nan
    ls = [ard,qrt,type_,loca,lat,lon,title,price,other_tags]
    browser.back()
    return ls

def get_listings_pages(browser, ard, qrt = None, n_pages = None):
    '''
    This functions runs through all the pages of listings and returns an array with the listings informations
    
    params
        browser: the selenium webdriver used to make requests
        ard: the district selected to land on listings page
        qrt: if it was used, the neighbourhood selected to land on listings page, otherwise None
        n_pages: the number of pages to scrape from listings pages, if None will scrape all pages
    '''
    
    listings_info = []
    if not on_listings_page(browser):
        raise Exception('Not a listings page')
    else:
        n_pages_avl = len(browser.find_elements_by_class_name('Dots'))
        if n_pages is None:
            last_page = False
            i=1 
            while not last_page:
                n_listings = len(browser.find_elements_by_xpath("//li[@class='listingBox w100']"))
                print(f'    should get {n_listings} listings from page {i}') #for debugging
                for n in range(n_listings):
                    ls = get_listing(browser,ard=ard,qrt=qrt,n=n)
                    listings_info.append(ls)
                try:
                    arrows = browser.find_elements_by_class_name('arrowDot')
                    arrows[1].click()  
                    i+=1
                except : 
                    last_page = True
            return listings_info
    
        else:
            if (n_pages > n_pages_avl) or (not isinstance(n_pages,int)) or (n_pages<=0):
                print(f'    n_pages must be positive integer smaller or equal to the number of pages, in this case {n_pages_avl}')
                n_pages = n_pages_avl
            for i in range(n_pages):
                n_listings = len(browser.find_elements_by_xpath("//li[@class='listingBox w100']"))
                print(f'should get {n_listings} listings form page {i}')
                for n in range(n_listings):
                    ls = get_listing(browser,ard=ard,qrt=qrt,n=n)
                    listings_info.append(ls)
                    pass
                try:
                    arrows = browser.find_elements_by_class_name('arrowDot')
                    arrows[1].click()   
                except : 
                    last_page = True
            return listings_info

def get_city_listings(browser,city,n_pages=None):
    '''
    This function return a dataframe with all the relevant property listings info scraped for a selected city

    Parameters
    ----------
    browser : webdriver
        The selenium webdriver used to make requests
    city : String
        The selected city to be scraped
    n_pages : int, optional
        The number of page to be scraped for each district or neihbourhood of the city The default is None.

    Returns
    -------
    df : DataFrame
        dataframe with following columns :
        'District','Neighbourhood','Type','Localisation','Latitude','Longitude','Title','Price','Tags'

    '''
    if not(isinstance(city,str)):
        raise TypeError('city must be of type string')
    else:
        
        all_data = []
        
        
        url = 'https://www.mubawab.ma/fr/mp/immobilier-a-vendre'
        browser.get(url)
        
        
        timeout = 20
        try:
            WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='na-map']")))
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()
        
        city = city.lower()
        city_buttons = browser.find_elements_by_xpath('//*[@id="top-villes"]/div/div/button')
        for button in city_buttons:
            if button.text.lower() == city.lower():
                click = button
        try:
            click.click()
        except:
            print(f'{city} not in top cities')
    
    timeout = 10
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='na-map']")))
    except TimeoutException:
        print("Timed out waiting for district page to load")
        browser.quit()
    
    url_ard = browser.current_url 
    n_arrondissements = len(browser.find_elements_by_xpath('/html/body/section/div[2]/div[1]/div[2]/ul/li')) 
    
    for n in range(1,n_arrondissements+1):
        arrondissement = browser.find_element_by_xpath(f'/html/body/section/div[2]/div[1]/div[2]/ul/li[{n}]/a') 
        ard_text = arrondissement.text
        arrondissement.click() 
        
        if on_listings_page(browser): 
            print(f'getting listings for {ard_text}') 
            all_data.append(get_listings_pages(browser, ard=ard_text,n_pages = n_pages)) 
            browser.get(url_ard) 
        else:
            url_qrt = browser.current_url 
            n_quartiers = len(browser.find_elements_by_xpath('/html/body/section/div[2]/div[1]/div[2]/ul/li')) 
            for nq in range(1,n_quartiers+1):
                quartier = browser.find_element_by_xpath(f'/html/body/section/div[2]/div[1]/div[2]/ul/li[{nq}]/a') 
                qrt_text = quartier.text 
                quartier.click()
                
                print(f'getting listings for {ard_text}, {qrt_text}') 
                all_data.append(get_listings_pages(browser,ard = ard_text, qrt= qrt_text,n_pages = n_pages)) 
                browser.get(url_qrt) 
            browser.get(url_ard) 
    df = pd.concat([pd.DataFrame(lst) for lst in all_data]).reset_index(drop = True)
    df.columns = ['District','Neighbourhood','Type','Localisation','Latitude','Longitude','Title','Price','Tags']
    
    return df

        

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.geolocation": 1
})


driver_path = r"C:\Users\R.BENZARIA\Downloads\chrome-win32\chrome-win32\chrome_proxy.exe"
service = Service(executable_path=driver_path)  
browser = webdriver.Chrome(service=service, options=options)


df = get_city_listings(browser,'Casablanca',n_pages = 1)
df.to_csv('mubawab_listings.cvs',index=False)

