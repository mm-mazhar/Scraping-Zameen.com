# import libraries
import warnings
warnings.filterwarnings("ignore")
import configparser
## Use selenium==4.0.0
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
import csv
import time
import os

conf = configparser.ConfigParser()
conf.read( 'conf.ini' )

#####################################################
############# Chrome Driver Setup ###################
#####################################################

chrome_driver = conf['settings']['chrome_driver']
base_url = conf['settings']['base_url']
no_of_webpages = int( conf['settings']['page_nums'] )

options = Options()
options.add_experimental_option( "detach", True )

print( "Initializing Chrome Drivers....." )
# service = Service( executable_path = chrome_driver )
# driver = webdriver.Chrome( service = service, options = options )
driver = webdriver.Chrome( executable_path = chrome_driver, options = options )

driver.get( base_url )
print( "Title: ", driver.title )
driver.maximize_window()
time.sleep( 5 )

#####################################################
############# Killing Popups or iFrames #############
#####################################################
print( "Killing Popups or iFrames ....." )

# #Killing iframes
# driver.switch_to.frame("google_ads_iframe_/31946216/Splash_660x500_0") # first frame
# driver.find_element(By.CLASS_NAME, "close_cross_big").click()

# #Switch back to main content
# driver.switch_to.default_content()
# driver.find_element(By.ID, "Path-3-Copy").click()
# driver.find_element(By.XPATH, "/html/body/div[2]/img").click()

# #Killing iframes again
# driver.switch_to.frame("google_ads_iframe_/31946216/HStrip_NS_0") # 2nd frame
# driver.find_element_by_xpath('/html/body/div[2]/img').click()

# #Switch back to main content
# driver.switch_to.default_content()

#Killing iframes
try:
    driver.switch_to.frame("google_ads_iframe_/31946216/Splash_660x500_0") # first frame
    driver.find_element_by_xpath('/html/body/div[2]/img').click()
except Exception as e:
    print( "Exception 1:", e )

#Switch back to main content
try:
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//*[@id="body-wrapper"]/div[2]/div/div/div[2]/button[2]').click()
except Exception as e:
    print( "Exception 2:", e )

#Killing iframes again
try:
    driver.switch_to.frame("google_ads_iframe_/31946216/HStrip_NS_0") # 2nd frame
    driver.find_element_by_xpath('/html/body/div[2]/img').click()
except Exception as e:
    print( "Exception 3:", e )

#Switch back to main content
driver.switch_to.default_content()

#####################################################
######## Extracting All the Links on Website ########
#####################################################
print( "Extracting Web Pages Links ....." )

page_listings = driver.find_elements_by_class_name('ef447dde')
print( "Per Page Listings Length: ", len(page_listings) )
links = []

count = 1

while count < no_of_webpages:
    print( f"Extracting Property Pages Links from Each Web Page {count}" )
    #print("count: ", count)
    driver.get( "https://www.zameen.com/Homes/Karachi-2-"+str(count)+".html" )
    time.sleep( 1 )
    for i in tqdm( range(len(page_listings)) ):
        #time.sleep( 2 )
        #print( "i: ", i )
        try:
            link = []
            page_listings = driver.find_elements_by_class_name('ef447dde')
            web_link = page_listings[i].find_elements_by_tag_name('a')[-6]
            web_link = web_link.get_property('href')
            link.append(web_link)
            links.append(link)
        except Exception as e:
            links.append(e)
        
    
    count +=1


print( "### Writing to CSV File ....." )    
web_pages_links = conf['settings']['web_pages_links']
# Open CSV file in write mode with newline=''
with open( web_pages_links, mode = 'a', newline = '' ) as csv_file:
    try:
        # Create CSV writer
        csv_writer = csv.writer(csv_file)
        # Write data to CSV file
        csv_writer.writerows(links)
    except Exception as e:
        print( f"Error in writing csv: {e}" )
        pass

print( "### Web Pages Links Extraction Complete ####" )
driver.close()





