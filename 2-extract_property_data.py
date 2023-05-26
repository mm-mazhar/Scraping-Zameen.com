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
import datetime
import re
import os

conf = configparser.ConfigParser()
conf.read( 'conf.ini' )

#####################################################
############# Chrome Driver Setup ###################
#####################################################

print( "Initializing Chrome Drivers....." )
chrome_driver = conf['settings']['chrome_driver']
options = Options()
options.add_experimental_option( "detach", True )
# service = Service( executable_path = chrome_driver )
# driver = webdriver.Chrome( service = service, options = options )
driver = webdriver.Chrome( executable_path = chrome_driver, options = options )

############# END Chrome Driver Setup ################

#####################################################
############# CSV Files To Read/Write Data ##########
#####################################################

print( "Processing CSV Files to Read and Write Data....." )
# Define the File Name and Headers To Write Property Data
property_data_csv = conf['settings']['property_data_csv']
headers = ["Date", "Title", "Location1", "Location2", "Type", "Bedrooms", "Bathrooms", "Size", "Purpose", "Price",
           "Built in year", "Parking Spaces", "Floors in Building", "Elevators", "Other Main Features", "Store Rooms",
           "Other Business and Communication Facilities", "Other Community Facilities", "Other Healthcare and Recreation Facilities",
           "Lobby in Building", "Double Glazed Windows", "Central Air Conditioning", "Central Heating", "Waste Disposal", "Furnished", 
           "Service Elevators in Building", "Flooring", "Electricity Backup", "Servant Quarters", "Study Room", "Prayer Room", "Powder Room",
           "Gym", "Lounge or Sitting Room", "Laundry Room", "Business Center or Media Room in Building", "Satellite or Cable TV Ready",
           "Broadband Internet Access", "Intercom", "Conference Room in Building", "Community Swimming Pool", "Community Lawn or Garden",
           "Community Gym", "Community Center", "First Aid or Medical Centre", "Day Care center", "Kids Play Area", "Mosque",
           "Barbeque Area", "Lawn or Garden", "Swimming Pool", "Sauna", "Jacuzzi", "Nearby Schools", "Nearby Hospital",
           "Nearby Shopping Malls", "Nearby Restaurants", "Nearby Public Transport Service", "Other Nearby Places",
           "Security Staff", "Maintainance Staff", "Laundry or Dry Cleaning Facility", "Facilities for Disabled",
           "Property Link"]


# Open the CSV file and write headers
with open( property_data_csv, 'a', newline = '' ) as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer( csv_file )
    # Write the headers to the CSV file
    csv_writer.writerow( headers )

# Open the CSV file To Read Web Pages Links
web_pages_links = conf['settings']['web_pages_links']
with open( web_pages_links, 'r' ) as csv_file:
    # Create a CSV reader object
    csv_reader = csv.reader( csv_file )
    # Create a list to store the rows
    lst_web_pages_links = []
    # Loop through each row in the CSV file
    for row in csv_reader:
        # Append the row to the list of rows
        lst_web_pages_links.append( row )
        

print( f"Total Number of Properties: {len(lst_web_pages_links)}" )

############# END CSV File To Read/Write Data ########

#####################################################
############# Extracting Property Data ##############
#####################################################

print( "Extracting Property Data....." )

for link in tqdm( range(15189, len(lst_web_pages_links) ) ):
    # print(f"Extracting Property Data of {lst_web_pages_links[link][0]} ")
    
    driver.get( lst_web_pages_links[link][0] )
    print( "Page Title: ", driver.title )
    # driver.maximize_window()
    time.sleep( 2 )
    
    #Killing iframes
    try:
        # driver.switch_to.frame("google_ads_iframe_/31946216/HStrip_NS_0") # first frame
        driver.find_element(By.CLASS_NAME, "hotstrip_cross").click()
    except Exception as e:
        # print("Excetion in Killing iframes: ", e)
        print("Excetion in Killing iframes: ")
    
    #Extracting Features
    try:
        date_time = datetime.datetime.now()
    except Exception as e:
        date_time = "NaN"
    
    try:
        title = driver.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[2]/div/div[1]/h1').text
    except Exception as e:
        title = "NaN"
        
    try:
        location1 = driver.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[2]/div/div[1]/div').text
    except Exception as e:
        location1 = "NaN"
        
    try:
        location2 = driver.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div[1]/div/div[2]/ul/li[3]').text
    except Exception as e:
        location2 = "NaN"
        
    try:    
        type_of_property = driver.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div[1]/div/div[2]/ul/li[1]/span[2]').text
    except Exception as e:
        type_of_property = "NaN"
    
    try:
        bedrooms = driver.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div[1]/div/div[2]/ul/li[7]/span[2]').text
    except Exception as e:
        bedrooms = "NaN"
    
    try:
        bathrooms = driver.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div[1]/div/div[2]/ul/li[4]/span[2]').text
    except Exception as e:
        bathrooms = "NaN"
    
    try:
        area_covered = driver.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div[1]/div/div[2]/ul/li[5]/span[2]/span').text
    except Exception as e:
        area_covered = "NaN"
    
    try:
        purpose = driver.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div[1]/div/div[2]/ul/li[6]/span[2]').text
    except Exception as e:
        purpose = "NaN"

    try:
        price = driver.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div[1]/div/div[2]/ul/li[2]/span[2]').text
    except Exception as e:
        price = "NaN"
        
    #Click Amenities 'View More' Button
    try:
        driver.switch_to.default_content()
        driver.find_element(By.CLASS_NAME, "_2f838ff4").click()
    except Exception as e:
        # print( "Exception in Amenities (View More):", e )
        print( "Exception in Amenities (View More):", e)
    
    try:
        amenities = driver.find_element(By.CLASS_NAME, "_0bde6dbc").text
    except Exception as e:
        amenities = "NaN"
    
    try:
        view = int(re.findall(r'View: (\d+)', amenities)[0]) if re.search(r'View: \d+', amenities) else None
    except AttributeError:
        view = "NaN"
    
    try:
        pattern = r"Built in year:\s*(.*)"
        matches = re.findall(pattern, amenities)
        if matches:
            built_in_year = matches[0]
        else:
            built_in_year = None
    except AttributeError:
        built_in_year = "NaN"

    try:    
        parking_spaces = int(re.findall(r'Parking Spaces: (\d+)', amenities)[0]) if re.search(r'Parking Spaces: \d+', amenities) else None
    except AttributeError:
        parking_spaces = "NaN"
        
    try:    
        floors_in_Building = int(re.findall(r'Floors in Building: (\d+)', amenities)[0]) if re.search(r'Floors in Building: \d+', amenities) else None
    except AttributeError:
        floors_in_Building = "NaN"

    try:    
        elevators = int(re.findall(r'Elevators: (\d+)', amenities)[0]) if re.search(r'Elevators: \d+', amenities) else None
    except AttributeError:
        elevators = "NaN"
        
    try:
        pattern = r"Other Main Features:\s*(.*)"
        matches = re.findall(pattern, amenities)
        if matches:
            other_main_features = matches[0]
        else:
            other_main_features = None
    except AttributeError:
        other_main_features = "NaN"
        
    try:    
        store_rooms = int(re.findall(r'Store Rooms: (\d+)', amenities)[0]) if re.search(r'Store Rooms: \d+', amenities) else None
    except AttributeError:
        store_rooms = "NaN"
        
    try:
        pattern = r"Other Business and Communication Facilities:\s*(.*)"
        matches = re.findall(pattern, amenities)
        if matches:
            other_business_and_communication_facilities = matches[0]
        else:
            other_business_and_communication_facilities = None
    except AttributeError:
        other_business_and_communication_facilities = "NaN"
        
    try:
        pattern = r"Other Community Facilities:\s*(.*)"
        matches = re.findall(pattern, amenities)
        if matches:
            other_community_facilities = matches[0]
        else:
            other_community_facilities = None
    except AttributeError:
        other_community_facilities = "NaN"

    try:
        pattern = r"Other Healthcare and Recreation Facilities:\s*(.*)"
        matches = re.findall(pattern, amenities)
        if matches:
            other_healthcare_and_recreation_facilities = matches[0]
        else:
            other_healthcare_and_recreation_facilities = None
    except AttributeError:
        other_healthcare_and_recreation_facilities = "NaN"

    try:  
        lobby_in_building = re.search(r'Lobby in Building', amenities) is not None
    except AttributeError:
        lobby_in_building = "NaN"

    try:
        double_glazed_windows = re.search(r'Double Glazed Windows', amenities) is not None
    except AttributeError:
        double_glazed_windows = "NaN"
        
    try:
        central_air_conditioning = re.search(r'Central Air Conditioning', amenities) is not None
    except AttributeError:
        central_air_conditioning = "NaN"

    try:
        central_heating = re.search(r'Central Heating', amenities) is not None
    except AttributeError:
        central_heating = "NaN"
        
    try:
        waste_disposal = re.search(r'Waste Disposal', amenities) is not None
    except AttributeError:
        waste_disposal = "NaN"
        
    try:
        furnished = re.search(r'Furnished', amenities) is not None
    except AttributeError:
        furnished = "NaN"
        
    try:
        service_elevators_in_building = re.search(r'Service Elevators in Building', amenities) is not None
    except AttributeError:
        service_elevators_in_building = "NaN"
        
    try:
        flooring = re.search(r'Flooring', amenities) is not None
    except AttributeError:
        flooring = "NaN"
        
    try:
        electricity_backup = re.search(r'Electricity Backup', amenities) is not None
    except AttributeError:
        electricity_backup = "NaN"

    try:
        servant_quarters = re.search(r'Servant Quarters', amenities) is not None
    except AttributeError:
        servant_quarters = "NaN"

    try:
        study_room = re.search(r'Study Room', amenities) is not None
    except AttributeError:
        study_room = "NaN"

    try:
        prayer_room = re.search(r'Prayer Room', amenities) is not None
    except AttributeError:
        prayer_room = "NaN"

    try:
        powder_room = re.search(r'Powder Room', amenities) is not None
    except AttributeError:
        powder_room = "NaN"
        
    try:
        gym = re.search(r'Gym', amenities) is not None
    except AttributeError:
        gym = "NaN"

    try:
        steam_room = re.search(r'Steam Room', amenities) is not None
    except AttributeError:
        steam_room = "NaN"

    try:
        lounge_or_sitting_room = re.search(r'Lounge or Sitting Room', amenities) is not None
    except AttributeError:
        lounge_or_sitting_room = "NaN"
        
    try:
        laundry_room = re.search(r'Laundry Room', amenities) is not None
    except AttributeError:
        laundry_room = "NaN"

    try:
        business_center_or_media_room_in_building = re.search(r'Business Center or Media Room in Building', amenities) is not None
    except AttributeError:
        business_center_or_media_room_in_building = "NaN"

    try:
        satellite_or_cable_tv_ready = re.search(r'Satellite or Cable TV Ready', amenities) is not None
    except AttributeError:
        satellite_or_cable_tv_ready = "NaN"
        
    try:
        broadband_internet_access = re.search(r'Broadband Internet Access', amenities) is not None
    except AttributeError:
        broadband_internet_access = "NaN"

    try:
        intercom = re.search(r'Intercom', amenities) is not None
    except AttributeError:
        intercom = "NaN"
        
    try:
        conference_room_in_building = re.search(r'Conference Room in Building', amenities) is not None
    except AttributeError:
        conference_room_in_building = "NaN" 
        

    try:
        community_swimming_pool = re.search(r'Community Swimming Pool', amenities) is not None
    except AttributeError:
        community_swimming_pool = "NaN" 
        
    try:
        community_lawn_or_garden = re.search(r'Community Lawn or Garden', amenities) is not None
    except AttributeError:
        community_lawn_or_garden = "NaN" 

    try:
        community_gym = re.search(r'Community Gym', amenities) is not None
    except AttributeError:
        community_gym = "NaN"
        
    try:
        community_center = re.search(r'Community Centre', amenities) is not None
    except AttributeError:
        community_center = "NaN"
            
    try:
        first_aid_or_medical_centre = re.search(r'First Aid or Medical Centre', amenities) is not None
    except AttributeError:
        first_aid_or_medical_centre = "NaN"
        
    try:
        day_care_center = re.search(r'Day Care Centre', amenities) is not None
    except AttributeError:
        day_care_center = "NaN"
            
    try:
        kids_play_area = re.search(r'Kids Play Area', amenities) is not None
    except AttributeError: 
        kids_play_area = "NaN"
        
    try:
        mosque = re.search(r'Mosque', amenities) is not None
    except AttributeError:
        mosque = "NaN"
        
    try:
        barbeque_area = re.search(r'Barbeque Area', amenities) is not None
    except AttributeError:
        barbeque_area = "NaN"

    try:
        lawn_or_garden = re.search(r'Lawn or Garden', amenities) is not None
    except AttributeError:
        lawn_or_garden = "NaN"

    try:
        swimming_pool = re.search(r'Swimming Pool', amenities) is not None
    except AttributeError:
        swimming_pool = "NaN"
        
    try:
        sauna = re.search(r'Sauna', amenities) is not None
    except AttributeError:
        sauna = "NaN"
        
    try:
        jacuzzi = re.search(r'Jacuzzi', amenities) is not None
    except AttributeError:
        jacuzzi = "NaN"

    try:
        nearby_schools = re.search(r'Nearby Schools', amenities) is not None
    except AttributeError:
        nearby_schools = "NaN" 
        
    try:
        nearby_hospital = re.search(r'Nearby Hospital', amenities) is not None
    except AttributeError:
        nearby_hospital = "NaN"     

    try:
        nearby_shopping_malls = re.search(r'Nearby Shopping Malls', amenities) is not None
    except AttributeError:
        nearby_shopping_malls = "NaN" 

    try:
        nearby_restaurants = re.search(r'Nearby Restaurants', amenities) is not None
    except AttributeError:
        nearby_restaurants = "NaN"

    try:
        nearby_public_transport_service = re.search(r'Nearby Public Transport Service', amenities) is not None
    except AttributeError:
        nearby_public_transport_service = "NaN" 

    try:
        other_nearby_places = re.search(r'Other Nearby Places', amenities) is not None
    except AttributeError:
        other_nearby_places = "NaN" 
        
    try:
        security_staff = re.search(r'Security Staff', amenities) is not None
    except AttributeError:
        security_staff = "NaN" 

    try:
        maintainance_staff = re.search(r'Maintenance Staff', amenities) is not None
    except AttributeError:
        maintainance_staff = "NaN" 

    try:
        laundry_or_dry_cleaning_facility = re.search(r'Laundry or Dry Cleaning Facility', amenities) is not None
    except AttributeError:
        laundry_or_dry_cleaning_facility = "NaN" 
        
    try:
        facilities_for_disabled = re.search(r'Facilities for Disabled', amenities) is not None
    except AttributeError:
        facilities_for_disabled = "NaN" 
        
        
    temp = [date_time, title, location1, location2, type_of_property, bedrooms, bathrooms, area_covered, purpose, price, 
           built_in_year, parking_spaces, floors_in_Building, elevators, other_main_features, store_rooms, other_business_and_communication_facilities,
           other_community_facilities, other_healthcare_and_recreation_facilities, lobby_in_building, double_glazed_windows, central_air_conditioning, 
           central_heating, waste_disposal, furnished, service_elevators_in_building, flooring, electricity_backup, servant_quarters, study_room, 
           prayer_room, powder_room, gym, lounge_or_sitting_room, laundry_room, business_center_or_media_room_in_building, satellite_or_cable_tv_ready,
           broadband_internet_access, intercom, conference_room_in_building, community_swimming_pool, community_lawn_or_garden, community_gym, 
           community_center, first_aid_or_medical_centre, day_care_center, kids_play_area, mosque, barbeque_area, lawn_or_garden, swimming_pool, sauna,
           jacuzzi, nearby_schools, nearby_hospital, nearby_shopping_malls, nearby_restaurants, nearby_public_transport_service, other_nearby_places,
           security_staff, maintainance_staff, laundry_or_dry_cleaning_facility, facilities_for_disabled,
           lst_web_pages_links[link][0]]
    
    # Open the CSV file and write 'temp'
    with open( property_data_csv, 'a', newline = '' ) as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer( csv_file )
        # Write the 'temp'to the CSV file
        csv_writer.writerow( temp )
        
driver.close()
    