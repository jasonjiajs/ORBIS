# this script is used to download all the PDF files from Chiefs of State directory
# The target is the CIA website.
# Also store the country list for identification purpose


import requests
from bs4 import BeautifulSoup

Target_Site = "https://www.cia.gov/library/publications/resources/world-leaders-1/"

month_dict = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}

# get the website source code
html_content = requests.get(Target_Site)

# Turn into a beautiful soup object
html_text = BeautifulSoup(html_content.content, features="html.parser")

# Find the ideal source
country_directory = html_text.find('ul', attrs={'id': 'cosCountryList'})

country_list = country_directory.find_all('a')

# the result set
country_update = []

country_num = 0
country_num_na = 0


# country list
outPath = 'C:\\Users\\stang10\\Dropbox\\data sample'

file_name = outPath + '\\' + 'country_list.txt'

output_file = open(file_name, 'w', errors='ignore')

# for each country in country_list, get the country name and read the href, and then search for the updated time
for country_obj in country_list:
    print(country_obj)
    country_name = country_obj.string
    print(country_name.lower(), file=output_file)
    fullurl = Target_Site + country_obj.get('href')
    print(fullurl)
    country_website = BeautifulSoup(requests.get(fullurl).content, features='html.parser')
    update_time = country_website.find('span', attrs={'id': 'lastUpdateDate'}).get_text()
    # now we get a string for each country, the string could either be N/A or a day-month-year combination
    time = update_time.split()
    if "N/A" != time[0]:
        day = int(time[0])
        month = month_dict[time[1]]
        year = int(time[2])
        country_tuple = (country_name, year, month, day)
        country_update.append(country_tuple)
    else:
        country_update.append((country_name,9999,9999,9999))   # 9999 stands for missing values
        country_num_na += 1
    country_num += 1

country_update.sort(key = lambda X: [X[1], X[2], X[3]])

print(country_update)
print(country_num)
print(country_num_na)

output_file.close()