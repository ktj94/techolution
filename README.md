# techolution
scraped and sorted data from Techolution Careers website.

To run, use python3

> python3 techolution.py

Dependencies-
pandas
selenium

To install the dependencies:

> pip3 install pandas
> pip3 install selenium

If some error occours with the chromedriver download it from here http://chromedriver.chromium.org/downloads

Extract and save it to same location where the "techolution.py" file is present.

If using in on a linux machine you might need to give execute permission to it. To do this run the following command:

> chmod +x chromedriver.

the final sorted and saved file will be created on same directory where the "techolution.py" file is present, with the name of "techolution.csv".

You could delete the "temp_df.csv" and "techolution.csv" before running the "techolution.py" file



At first i tried to scrap with Requests/urllib.Requests but it didn't work with CSS classes, so have to switch to Selenium.

Also to sorting the data I've used current date-time as a base or a starting point from where the time posted will be calculated.
