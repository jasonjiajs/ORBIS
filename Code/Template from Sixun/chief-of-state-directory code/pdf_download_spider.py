# this script is used to download all the PDF files from Chiefs of State directory
# The target is the CIA website.


import requests
from bs4 import BeautifulSoup

Target_Site = "https://www.cia.gov/library/publications/resources/world-leaders-1/"
output_directory = "C:/Users/stang10/Dropbox/data sample/chiefsofstate"
# get the website source code
html_content = requests.get(Target_Site)

# Turn into a beautiful soup object
html_text = BeautifulSoup(html_content.content, features="html.parser")

# Find the ideal source
ym_directory = html_text.find_all('a', attrs={'target': '_new'})

# for links inside the directory, open and save
for i, link in enumerate(ym_directory):
    full_url = Target_Site + link.get('href')
    # Generate the name of the file by year and month
    year = str(link.get('href'))[5:9]
    month = link.get_text()
    name = year + month
    # save files with name containing year and month
    if full_url.endswith('.pdf'):
        file_name = output_directory + '/' + name + '.pdf'
        with open(file_name, 'wb') as f:
            file_source = requests.get(full_url)
            f.write(file_source.content)
            f.close()
        print("%s for year %s is saved" % (month, year))
