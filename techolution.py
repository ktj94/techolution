import os
import pandas as pd
from selenium import webdriver
from datetime import datetime
from dateutil.relativedelta import relativedelta


def scrape_data(driver_path ,save_path):
    print("Scraping Data ...")

    url = "https://techolution.app.param.ai/jobs/"
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(executable_path=driver_path ,options=op)
    driver.get(url)
    driver.implicitly_wait(20)

    # retriving the data which is present inside the class "job_list_card".
    divs=driver.find_elements_by_class_name('job_list_card')

    # some cleaning
    data=[]
    for div in divs:
        temp_text = div.text.replace('·', '\n')
        list1 = temp_text.split('\n')
        entry = [word.strip() for word in list1]
        data.append(entry)
    # print(data)

    # adding appropriate coloumn headers.
    df = pd.DataFrame(data, columns=('Position', 'Type', 'Location', 'Experience', 'Time posted'))

    # save this temporary dataframe to csv,  so that we need not to scrape whole site again.
    df.to_csv(save_path, index=False)
    print("Done, scraping...")

def clean_save_data(load_path,save_final):
    print("\nCleaning and sorting data")
    df = pd.read_csv(load_path)

    # adding an extra coloumn which will be used for sorting.
    df['Time stamp']=df['Time posted']
    temp_list = df["Time stamp"].tolist()

    # using current time as the base in which the time of job posts will be added.
    cur_time = datetime.now()
    
    time_stamp_list=[]
    for time in temp_list:
        a = time.split()
        
        if a[0] in ['a','an']:
            a[0] = 1
            
        a = [int(a[0]), a[1]]
        
        if a[1].lower() in ['hour', 'hours']:
            a[1] = cur_time + relativedelta(hours=a[0])
        elif a[1].lower() in ['days', 'day']:
            a[1] = cur_time + relativedelta(days=a[0])
        elif a[1].lower() in ['months', 'month']:
            a[1] = cur_time + relativedelta(months=a[0])
        elif a[1].lower() in ['years', 'year']:
            a[1] = cur_time + relativedelta(years=a[0])
        time_stamp_list.append(a[1])

    df["Time stamp"] = pd.DataFrame(time_stamp_list)

    # sorting the data frame.
    df = df.sort_values(by=['Time stamp'],ascending=False)

    # removing the coloumn which was added earlier.
    df = df.drop(['Time stamp'], axis= 1)
    # print(df)

    # saving the final sorted data.
    df.to_csv(save_final, index=False)

if __name__=="__main__":
    # get current directory (independent of the OS)
    cwd = os.getcwd()
    driver_path = os.path.join(cwd,"chromedriver")
    save_path = os.path.join(cwd,'temp_df.csv')
    scrape_data(driver_path, save_path)

    final_data = os.path.join(cwd,'techolution.csv')
    clean_save_data(save_path,final_data)
    print("\n Done, saved csv in {}".format(final_data))
