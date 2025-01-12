from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
import time

s = Service("C:/Users/priya/Downloads/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=s)

driver.get("https://collegedunia.com/india-colleges")

rank_list =[]
clg_name_list = []
clg_link_list = []
clg_location_list = []
clg_approval_list = []
clg_course_list = []
clg_fees_list = []
program_name_list = []
avg_pack_list = []
high_pack_list = []
clg_review_list = []
clg_tag_list = []
clg_ranking_list = []
ranking_out_of_list = []

def scrape(soup):
    table_wrapper = soup.find_all('div',class_= 'jsx-4033392124 jsx-1933831621 table-wrapper')
    for table in table_wrapper:
        tr_list = table.div.table.tbody.find_all('tr',recursive=False)
        for tr in tr_list:
            td_list = tr.find_all('td',recursive=False)
            for index,td in enumerate(td_list):
                if (index==0):
                    rank_list.append(int(td.text.lstrip('#')))
                if (index == 1):
                    clg_name_list.append(td.div.div.a["data-csm-title"])
                    clg_link_list.append(td.div.div.a["href"])
                    location = td.div.find('span',class_='jsx-3230181281 pr-1 location')
                    if(location):
                        clg_location_list.append(location.text.strip())
                    else:
                        clg_location_list.append('')
                    approval = td.div.find('span',class_='jsx-3230181281 approvals pl-1')
                    if(approval):
                        clg_approval_list.append(approval.text.replace("\xa0"," ").strip())
                    else:
                        clg_approval_list.append('')
                    course = td.div.find('span',class_='jsx-3230181281 course-name')
                    if(course):
                        clg_course_list.append(course.text.strip())
                    else:
                        clg_course_list.append('')
                if(index == 2):
                    fees = td.a.find('span',class_="jsx-3230181281 text-lg text-green d-block font-weight-bold mb-1")
                    if(fees):
                        clg_fees_list.append(int(fees.text[2:].replace(',','').strip()))
                    else:
                        clg_fees_list.append('')
                    program = td.a.find('span',class_="jsx-3230181281 fee-shorm-form")
                    if(program):
                        program_name_list.append(program.text.strip())
                    else:
                        program_name_list.append('')
                if(index == 3):
                    package = td.find_all('span', class_="jsx-914129990 text-green d-block mb-1")
                    if len(package) == 2:
                        avg = package[0]
                        high = package[1]
                        avg_pack_list.append(int(avg.text[2:].replace(',', '').strip()) if avg else '')
                        high_pack_list.append(int(high.text[2:].replace(',', '').strip()) if high else '')
                    elif len(package) == 1:
                        avg_pack_list.append('')
                        high = package[0]
                        high_pack_list.append(int(high.text[2:].replace(',', '').strip()) if high else '')
                    else:
                        avg_pack_list.append('')
                        high_pack_list.append('')
                if(index == 4):
                    review = td.find('span',class_='jsx-3230181281 lr-key text-lg text-primary d-block font-weight-medium mb-1')
                    if(review):
                        clg_review_list.append(review.text.strip())
                    else:
                        clg_review_list.append('')
                    rv = td.find('span',class_='jsx-3230181281 placement-reviews-back pointer position-relative p-1 tagline mt-2 font-weight-medium d-inline-flex align-items-center')
                    if(rv):
                        tag = rv.find('span',class_='jsx-3230181281')
                        if(tag):
                            clg_tag_list.append(tag.text)
                        else:
                            clg_tag_list.append('')
                    else:
                        clg_tag_list.append('')
                if(index == 5):
                    rnk = td.find('span',class_='jsx-2794970405 rank-span no-break')
                    if(rnk):
                        ranking = rnk.find('span',class_='jsx-2794970405')
                        if(ranking):
                            clg_ranking_list.append(int(ranking.text.split('th')[0].replace('#', '')))
                            ranking_out_of_list.append(int((ranking.find('span',class_='jsx-2794970405 text-primary').text)))
                        else:
                            clg_ranking_list.append('')
                            ranking_out_of_list.append('')
                    else:
                        clg_ranking_list.append('')
                        ranking_out_of_list.append('')

# Automatically scroll the page
scroll_pause_time = 0.1  # Pause between each scroll
screen_height = driver.execute_script("return window.screen.height;")  # Browser window height
i = 1
max_scroll_time = 30
start_time = time.time()
while True:
    # Scroll down
    driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
    i += 1
    time.sleep(scroll_pause_time)

    # Check if reaching the end of the page
    # scroll_height = driver.execute_script("return document.body.scrollHeight;")
    # if screen_height * i > scroll_height:
    #     break
    if time.time() - start_time > max_scroll_time:
        break 

# Fetch the data using BeautifulSoup after all data is loaded
soup = BeautifulSoup(driver.page_source, "html.parser")
scrape(soup)

# Process and save the data as needed

# Close the WebDriver session
driver.quit()



            



scraped_data = {
    "Rank": rank_list,
    "Colleges": clg_name_list,
    "Website": clg_link_list,
    "Location": clg_location_list,
    "Approval": clg_approval_list,
    "Course":clg_course_list,
    "Fees": clg_fees_list,
    "Program Name": program_name_list,
    "Average Package": avg_pack_list,
    "Highest Package": high_pack_list,
    "User Review": clg_review_list,
    "Tags": clg_tag_list,
    "College Ranking": clg_ranking_list,
    "Out of (Total Colleges)": ranking_out_of_list
}
df = pd.DataFrame(scraped_data)
df.to_excel('TopColleges2025India.xlsx',index=False)
print("Done Boss")