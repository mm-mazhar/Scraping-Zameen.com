# #import libraries
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import re
import configparser
conf = configparser.ConfigParser()
print(conf.read( 'conf.ini' ))


# #To visualise al the columns in the dataframe
pd.pandas.set_option('display.max_columns', None)
pd.pandas.set_option('display.max_rows', 10)


# #define the conversion function
def convert_to_millions(x):
    search_digits = r'\d*\.?\d+'
    substring_1 = "Crore"
    substring_2 = "Lakh"
    x = str(x) # convert to string #to fix the error 'expected string or bytes-like object'
    match = re.search(search_digits, x)
    if match:
        tmp = float(match.group(0))
        if substring_1 in x:
            return round(tmp*10e6, 2)/1e6
        if substring_2 in x:
            return round(tmp*0.1, 2)
    else:
        tmp = 'NaN'
        return tmp
    

# # Define function to check the length of the string
def filter_len(x):
    if len(x) == 4:
        return x
    else:
        return np.nan


#########################################################################
############# Reading CSV and Display Basis Stuff #######################
#########################################################################
print("\nReading CSV and Display Basic Stuff............................")
data = pd.read_csv(conf['settings']['property_data_csv'])

# #Droping Un-necessary Columns
columns_to_drop = ['Date', 'Title', 'Purpose', 'Other Main Features', 'Other Business and Communication Facilities', \
                   'Other Community Facilities', 'Other Healthcare and Recreation Facilities', 'Property Link']

data.drop(columns = columns_to_drop, axis = 1, inplace = True)

# #Info
print(data.info())

# #Columns
print(data.columns)

#########################################################################
############# Check Missing Values ######################################
#########################################################################
print("\nChecking Missing Values........................................")
for i in data.columns:
    # #Replace the missing values with NaN
    data[i].fillna(np.nan, inplace = True)
    if data[i].isnull().sum() > 0:
        print("\nMissing Values in Column Name: ", i)
        print(data[i].isnull().sum())   

# #Copy DF       
df = data.copy()

#########################################################################
######### Cast the column 'Parking Spaces' to numeric data type #########
#########################################################################
print("\nCasting column 'Parking Spaces' to numeric data type..........")
# #fill missing values with 0
df['Parking Spaces'].fillna(0, inplace = True)
# #replace 0 values with NaN
df['Parking Spaces'].replace('0', np.nan, inplace = True)
# #replace infinite values with NaN
df['Parking Spaces'].replace([np.inf, -np.inf], np.nan, inplace = True)
df['Parking Spaces'] = df['Parking Spaces'].astype(np.int32)

#########################################################################
######### Remove text from column 'Size' and cast as float type #########
#########################################################################
print("\nRemoving text from column 'Size' and cast as float type........")
#df.Size.unique()
# #remove text from column size
df['Size_in_SqYds'] = df['Size'].str.replace(' Sq. Yd.', '')
df['Size_in_SqYds'] = df['Size_in_SqYds'].str.replace(',', '')
df['Size_in_SqYds'] = df['Size_in_SqYds'].astype(np.float32)
df.drop('Size', axis = 1, inplace = True)
#df['Size_in_SqYds'].unique()

#########################################################################
### Droping Rows with df.Type containing 'Commercial Plot and others' ###
#########################################################################
print("\nDroping Rows with 'Type' col containing irelevant categories...")
print(df.Type.value_counts())
df = df[(df.Type == 'House') | (df.Type == 'Flat')]
print(df.Type.unique())

#########################################################################
########## Remove Text from column 'Bathrooms' and 'Bedrooms' ###########
#########################################################################
print("\nRemoving Text from column 'Bathrooms' and 'Bedrooms'...........")
#print(df.Bathrooms.value_counts())
#print(df.Bathrooms.dtype)
#df.Bathrooms.unique()
# #Define the pattern to match
# pattern = r'PKR.*?\d+(\.\d+)?\s*\w+'
pattern = r'PKR\s*\d+(\.\d+)?(?!\s*Rs)\s*\b'
# #Replace the matched pattern with an empty string
# df['Bathrooms'] = df['Bathrooms'].str.replace(pattern, '', regex = True)
# df['Bathrooms'].replace([np.inf, -np.inf], np.nan, inplace = True)
# df['Bathrooms'] = df['Bathrooms'].replace('-', np.nan)

df['Bathrooms'] = df['Bathrooms'].str.replace('\n', '')
df['Bathrooms'] = df['Bathrooms'].replace('-', np.nan)
df['Bathrooms'] = df['Bathrooms'].str.replace(pattern, '', regex = True)
df['Bathrooms'].replace([np.inf, -np.inf], np.nan, inplace = True)

# #Convert the column to numeric data type
df['Bathrooms'] = pd.to_numeric(df['Bathrooms'], errors = 'coerce')
print(df['Bathrooms'].dtype)
print(df.Bathrooms.unique())
#print(df.Bathrooms.value_counts())

#print(df.Bedrooms.value_counts())
#print(df.Bedrooms.dtype)
# #removing unnecessary text
df['Bedrooms'] = df['Bedrooms'].str.replace('\n', '')
df['Bedrooms'] = df['Bedrooms'].replace('-', np.nan)
# C#onvert the column to numeric data type
df['Bedrooms'] = pd.to_numeric(df['Bedrooms'], errors = 'coerce')
#print(df.Bedrooms.unique())
#print(df.Bedrooms.dtype)

#########################################################################
########### Converting 'Price' column to 'Price_in_millions' ############
#########################################################################
print("\nConverting 'Price' column to 'Price_in_millions'...............")
#print(df.Price.unique())
df['Price'] = df['Price'].str.replace('PKR\n', '')
# #create a new column 'price_in_millions' by applying the conversion function to 'price'
df['Price_in_millions'] = df['Price'].apply(lambda x: convert_to_millions(x))
# print(df[['Price','Price_in_millions']])
df.drop('Price', axis = 1, inplace = True)
#print(df.Price_in_millions.unique())

#########################################################################
######## Convert the column 'Built in year' into Date time object #######
#########################################################################
print("\nConvert the column 'Built in year' into Date time object........")
# #fill missing values with 0
df['Built in year'].fillna(0, inplace = True)
# #replace 0 values with NaN
df['Built in year'].replace('0', np.nan, inplace = True)
# #replace infinite values with NaN
df['Built in year'].replace([np.inf, -np.inf], np.nan, inplace = True)

# #cast the column to integer data type
df['Built in year'] = df['Built in year'].astype(int)
df['Built in year'] = df['Built in year'].astype(str)

#print(df['Built_in_year'].value_counts())
#print(df['Built in year'].unique())
    
# #replace with np.nauniquef number of digits in df['Built in year'] is less than 4 and greater than 4
df['Built_in_year'] = df['Built in year'].apply(lambda x: filter_len(x))

# #convert the column to datetime object
df['Built_in_year'] = pd.to_datetime(df['Built_in_year'] + '-01-01', errors = 'coerce')
df.drop('Built in year', axis = 1, inplace = True)

#print(df['Built_in_year'].unique())
#print(df['Built_in_year'].dtype)
#print(df['Built_in_year'].value_counts())
#print(df['Built_in_year'].value_counts().index)
#print(df['Built_in_year'])

#########################################################################
########### Removing Unnecessary text from column 'Location2' ###########
#########################################################################
print("\nRemoving Unnecessary text from column 'Location2'..............")
# Replace the missing values with NaN
df['Location2'].fillna(np.nan, inplace = True)
#print(len(df.Location2))
#print(df.Location2.nunique())
# #Removing unnecessary text
pattern = r'Initial Amount\nPKR\n.*'
df['Location2'] = df['Location2'].str.replace('Location\n', '')
df['Location2'] = df['Location2'].str.replace(', Karachi, Sindh', '')
df['Location2'] = df['Location2'].str.replace(pattern, "NaN", regex = True)
df['Location2'].replace("NaN", None, inplace = True)

#########################################################################
########### Removing Unnecessary text from column 'Location1' ###########
#########################################################################
print("\nRemoving Unnecessary text from column 'Location1'..............")
# pd.pandas.set_option('display.max_rows', 10)
# pd.pandas.set_option('display.max_columns', None)
print("Check Un-wanted Text: ", df.Location1[0:5][1])
df.Location1 = df.Location1.str.replace(", Karachi, Sindh", "")
print("Un-wanted Text Removed: ", df.Location1[0:5][1])
print("Check at Random Index: ", df.Location1[5271])

#########################################################################
########################## Reset Index ##################################
#########################################################################
print("\nReseting Index.................................................")
df.reset_index(inplace = True)

#########################################################################
########################## Re-Naming Columns ############################
#########################################################################
print("\nRe-Naming Columns..............................................")
df.rename(columns = {'index' : 'Ids', 'Parking Spaces' : 'Parking_Spaces', 'Floors in Building' : 'Floors_in_Building', 'Store Rooms' :' Store_Rooms', 
                     'Lobby in Building' : 'Lobby_in_Building', 'Double Glazed Windows' : 'Double_Glazed_Windows', 'Central Air Conditioning' : 'Central_Air_Conditioning', 
                     'Central Heating' : 'Central_Heating', 'Waste Disposal' : 'Waste_Disposal', 'Service Elevators in Building' : 'Service_Elevators_in_Building',
                     'Electricity Backup' : 'Electricity_Backup', 'Servant Quarters' : 'Servant_Quarters', 'Study Room' : 'Study_Room', 'Prayer Room' : 'Prayer_Room', 
                     'Powder Room' : 'Powder_Room', 'Lounge or Sitting Room' : 'Lounge_or_Sitting_Room', 'Laundry Room' : 'Laundry_Room', 
                     'Business Center or Media Room in Building' : 'Business_Center_or_Media_Room_in_Building', 'Satellite or Cable TV Ready' : 'Satellite_or_Cable_TV_Ready', 
                     'Broadband Internet Access' : 'Broadband_Internet_Access', 'Conference Room in Building' : 'Conference_Room_in_Building',
                     'Community Swimming Pool' : 'Community_Swimming_Pool', 'Community Lawn or Garden' : 'Community_Lawn_or_Garden', 'Community Gym' : 'Community_Gym', 
                     'Community Center' : 'Community_Center', 'First Aid or Medical Centre' : 'First_Aid_or_Medical_Centre', 'Day Care center' : 'Day_Care_center', 
                     'Kids Play Area' : 'Kids_Play_Area', 'Barbeque Area' : 'Barbeque_Area', 'Lawn or Garden' : 'Lawn_or_Garden', 'Swimming Pool' : 'Swimming_Pool',
                     'Nearby Schools' : 'Nearby_Schools', 'Nearby Hospital' : 'Nearby_Hospital', 'Nearby Shopping Malls' : 'Nearby_Shopping_Malls',
                     'Nearby Restaurants' : 'Nearby_Restaurants', 'Nearby Public Transport Service': 'Nearby_Public_Transport_Service', 'Other Nearby Places' : 'Other_Nearby_Places',
                     'Security Staff' : 'Security_Staff', 'Maintainance Staff' : 'Maintainance_Staff', 'Laundry or Dry Cleaning Facility' : 'Laundry_or_Dry_Cleaning_Facility', 
                     'Facilities for Disabled' : 'Facilities_for_Disabled',
                    }, inplace = True)

print(df.columns)

#########################################################################
########################## Re-Arrange Columns ###########################
#########################################################################
print("\nRe-Arranging Columns..........................................")
df = df.reindex(columns = ['Ids', 'Location1', 'Location2', 'Type', 'Bedrooms', 'Bathrooms', 'Size_in_SqYds', 'Price_in_millions', 'Built_in_year', 'Parking_Spaces', 
                           'Floors_in_Building', 'Elevators', 'Store_Rooms', 'Lobby_in_Building', 'Double_Glazed_Windows', 'Central_Air_Conditioning', 'Central_Heating', 
                           'Waste_Disposal', 'Furnished', 'Service_Elevators_in_Building', 'Flooring', 'Electricity_Backup', 'Servant_Quarters', 'Study_Room', 'Prayer_Room',
                           'Powder_Room', 'Gym', 'Lounge_or_Sitting_Room', 'Laundry_Room', 'Business_Center_or_Media_Room_in_Building', 'Satellite_or_Cable_TV_Ready', 
                           'Broadband_Internet_Access', 'Intercom', 'Conference_Room_in_Building', 'Community_Swimming_Pool', 'Community_Lawn_or_Garden', 'Community_Gym', 
                           'Community_Center', 'First_Aid_or_Medical_Centre', 'Day_Care_center', 'Kids_Play_Area', 'Mosque', 'Barbeque_Area', 'Lawn_or_Garden', 'Swimming_Pool', 
                           'Sauna', 'Jacuzzi', 'Nearby_Schools', 'Nearby_Hospital', 'Nearby_Shopping_Malls', 'Nearby_Restaurants', 'Nearby_Public_Transport_Service',
                           'Other_Nearby_Places', 'Security_Staff', 'Maintainance_Staff', 'Laundry_or_Dry_Cleaning_Facility', 'Facilities_for_Disabled',])


#########################################################################
################ Replace True with 1 and False with 0 ###################
#########################################################################
print("\nReplacinge True with 1 and False with 0........................")
print(df.columns[13:])
for i in df.columns[13:]:
    print("\nUnique Values in Column Name: ", i)
    print(df[i].unique()) 
    # Replace True with 1 and False with 0
    df[i] = df[i].replace(True, 1).astype(np.int32)
    df[i] = df[i].replace(False, 0).astype(np.int32)
    print(df[i].unique())
    print(df[i].dtype)
    
# #Info
print(df.info())

#########################################################################
###################### Loading data into csv ############################
#########################################################################
print("\nLoading into CSV..............................................")
df.to_csv(conf['settings']['data'], index = False)


print("\nFinished......................................................")





