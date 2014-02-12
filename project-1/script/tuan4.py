from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import time
import os
import re

### from polo code
def check_exists_by_partial_link_text(text):
        try:
                browser.find_element_by_partial_link_text(text)
        except NoSuchElementException:
                return False
        return True

### Tuan Le
### 02-06-2014
### For Question3
def question_3(url):
        #list and dictionary are already global by its nature
        #declartion as global here is not necessary, but we have it
        #here for clarity.
        #global question_text_url_dict
        #global question_text_answers_dict
        #global answer_list
        #global user_id_list #3-a
        #global num_upvote_list #3-c
        #global users_upvote_list #3-d
        if url.find("?share=1") == -1:
                url = url + '?share=1'
        
        browser.get(url)
        src_updated = browser.page_source
        src = ""

        #scroll down the page until the end is reached and no more questions
        #are loaded
        while src != src_updated:
                time.sleep(5)
                src = src_updated
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                src_updated = browser.page_source

        #to verify src_updated does containt new content that is loaded into
        #the page, scroll to the bottom, and run
        #src_updated.find("the Mayor position in Los Angeles as")
        #This should not return a -1

        soup = BeautifulSoup(src_updated)
        
        #extract questions' text and the URL of the question pages

        #Caution: Some question text has a special "star symbol" in front
        #which makes the decoding fails.
        #Ex: u'\u2605If Otis Rolley is elected Major of Baltimore ...'
        #When trying to run command "print", it said
        #UnicodeEncodeError: 'charmap' codec can't encode character
        # u'\u2605' in position 0: character maps to <undefined>

        #Fix: by using .encode('utf-8') => not sure if this is the right option
        question_list = soup.find_all(attrs={"class":"question_link"})
        #question_text_url_dict = {} #key-value: text-url
        #question_text_answers_dict = {} #key-value: text-answer list
        
        #Note that question_dict.keys() or question_dict.values()
        #return list where items appear in random order
        for question in question_list:
                question_text = question.get_text().encode('utf-8')
                question_url = domain + question['href']

                #debugging purpose
                print("\n")
                print("Question text: "+question_text)
                print("\n")
                print("Question url: "+question_url)
                
                if question_url.find("?share=1") == -1:
                        question_url = question_url + '?share=1'

                #save to dictionary [question_text:question_url]  
                #question_text_url_dict[question_text] = question_url.encode('utf-8')

                browser.get(question_url)
                question_content_updated = browser.page_source
                src = ""

                #scroll down the page until the end is reached and no more questions are loaded
                while src != question_content_updated:
                        time.sleep(5)
                        src = question_content_updated
                        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        question_content_updated = browser.page_source

                question_soup = BeautifulSoup(question_content_updated)
                answer_text_list = []
                answer_content_list = question_soup.find_all(attrs={"class":"answer_content"})
                for answer in answer_content_list:
                        if len(answer['class']) == 1:
                                answer_processed = answer.find_all(id = re.compile("container"))
                                if len(answer_processed) != 0:
                                        #The desired answer text will reside in answer_processed[0]
                                        #remove div clause that has junk at the end
                                        for div_item in answer_processed[0].find_all('div'):
                                                div_item.decompose() #remove div clause
                                                
                                        answer_text = answer_processed[0].get_text().encode('utf-8')
                                        answer_text_list.append(answer_text)
                                        #save to dictionary [question_text:answer_text_list]
                                        #question_text_answers_dict[question_text] = answer_text_list

                                        #debugging
                                        print("\n");
                                        print("Answer text: "+answer_text)

                #debugging => this prints very long text
                #print("\nquestion_text_answers_dict\n")
                #print(question_text_answers_dict)

                #Question 3-a
                extracted_user_id_list = []
                answer_user_list = question_soup.find_all(attrs={"class":"answer_user"})
                for answer in answer_user_list:
                        #since the person that gives the answer and the voter belong to the same answer sequence,
                        #we need to filter out the voters. The person who answers is the one with the first
                        #user tag appears in "answer" html sequence
                        user_url = domain + answer.find(attrs={"class":"user"}).get('href').encode('utf-8')
                        extracted_user_id_list.append(user_url)

                #debugging
                print("\nextracted_user_id_list\n")
                print(extracted_user_id_list)

                #Question 3-b
                extracted_answer_date_list = []
                answer_date_list = question_soup.find_all(attrs={"class":"answer_permalink"})
                for answer in answer_date_list:
                        answer_date = answer.get_text().encode('utf-8')
                        extracted_answer_date_list.append(answer_date)

                #debugging
                print("\nextracted_answer_date_list\n")
                print(extracted_answer_date_list)

                #Question 3-c
                extracted_num_upvote_list = []
                num_upvote_list = question_soup.find_all(attrs={"class":"rating_value"})
                for upvote in num_upvote_list:
                        num_upvote = upvote.get_text().encode('utf-8')
                        extracted_num_upvote_list.append(num_upvote)

                #debugging
                print("\nextracted_num_upvote_list\n")
                print(extracted_num_upvote_list)

                #Question 3-d
                #Step 1: Extract the text "x more"
                #               Extract answer_user which containts the list of voters
                #               Search class="more_link" tag from there to get the text
                #               Note: There are other unrelated links that have more_link
                #               We don't want to activate those. For example,
                #               We don't want to activate "More Related Questions" link
                #Step 2: Call browser.find_element_by_partial_link_text("x more").click()
                #        to active the link

                #users include both the person answers the question (first person
                #in the list) and the voters
                #browser.find_element_by_partial_link_text("more").click() #will through NotClickableException if we scroll down the page

                #more_link text must be visible to be clickable. Since we scroll down to the
                #bottom, we have to scroll up again before being able to click the text.
                #CAUTION: Not scroll up, get a WebDriverException at
                #browser.find_element_by_link_text(more_link_text).click()
                browser.execute_script("window.scrollTo(0, 0);")
                time.sleep(5) #give enough time to scroll to the top before trying to activate more_link
                
                user_list = question_soup.find_all(attrs={"class":"answer_user"})
                for user in user_list:
                        more_link_result = user.find(attrs={"class":"more_link"})
                        if more_link_result is not None:
                                more_link_text = more_link_result.get_text().encode('utf-8')
                                if check_exists_by_partial_link_text(more_link_text):
                                        link_object = browser.find_element_by_link_text(more_link_text).click()
                                        time.sleep(5) #enough time to load content from more_link before activating another link
                                        

                #load new page source                
                updated_page = browser.page_source
                updated_soup = BeautifulSoup(updated_page)

                list_of_answer_voter_list = updated_soup.find_all(attrs={"class":"answer_voters"})
                for element_of_list_of_answer_voter_list in list_of_answer_voter_list:
                        extracted_answer_voter_list = [] #answer_voter_list per answer
                        answer_voter_list = element_of_list_of_answer_voter_list.find_all(attrs={"class":"user"})
                        for answer_voter in answer_voter_list:
                                answer_voter_id = domain + answer_voter.get('href').encode('utf-8')
                                extracted_answer_voter_list.append(answer_voter_id)
                        #debugging
                        print("\nextracted_answer_voter_list")
                        print(extracted_answer_voter_list)
                
                

                #TODO: REMOVE THIS LINE
                time.sleep(1000) #have some time to examine the content manually
                


### Polo Lee
### 02-05-2014
### For Question2
### Basic idea: use recursive function to make a DFS (Depth First Search)
def question_2(url, w_left_name, w_left_url):
	about_url = url + '/about?share=1'
	browser.get(about_url)
	time.sleep(2)
	about_source = browser.page_source
	about_source = about_source.split('Child Topics')
	if len(about_source) < 2:
		return
	else:
		about_source = about_source[1]
		#To see the first word of this string:
		#  about_source.partition(' ')[0]
	soup_about = BeautifulSoup(about_source)
	topic_name_list = soup_about.find_all(attrs={"class":"topic_name"})
	for item in topic_name_list:
		w_topic_name = w_left_name + '\t' + item.get_text()
                #Government Leaders and Politicitions\tU.S. City Mayors
		
		fw_topic_names.write((w_topic_name + '\n').encode('utf-8'))
		
		topic_url = domain + item['href']
                #http://www.quora.com/U-S-City-Mayors
		
		w_topic_url = w_left_url + '\t' + topic_url
                #http://www.quora.com/Government-Leaders-and-Politicians\thttp://www.quora.com/U-S-City-Mayors
		
		fw_topic_urls.write((w_topic_url+'\n').encode('utf-8'))
		
		question_2(topic_url, w_topic_name, w_topic_url)


 
### Question 1
### Get from sample script
domain = 'http://www.quora.com'
chosen_topic = 'Government Leaders and Politicians'
top_level_topic = chosen_topic
top_level_url = domain + '/' + chosen_topic.replace(" ","-")

fw = open(chosen_topic.replace(" ","-")+'.html', mode='w')
# links_file_name = url[21:].split('?')[0]
# fw_links = open("links/" + links_file_name , mode='w')

# The path configuration depends on your computer
chromedriver = "C:\\seltests\\virtualenv-1.10.1\\Scripts\\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)
# browser = webdriver.Chrome()
browser.get(top_level_url+'?share=1')

# keep scrolling down until there is no new updates
# That is to get the whole page
src_updated = browser.page_source
src = ""
while src != src_updated:
	time.sleep(5)
	src = src_updated
	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	src_updated = browser.page_source

# Save the whole page in fw
# that is current_page4.html
html_source = browser.page_source
fw.write(html_source.encode('utf-8'))
fw.close()

# soup = BeautifulSoup(html_source)
# question_links = soup.find_all("h3")
# list_items = soup.find_all(attrs={"class":"pagedlist_item"})

# split_html = html_source.split("<h3>")
# count = 0
# for i in range(1,len(split_html)):
# 	part = split_html[i].split('</h3>')[0]
# 	part_soup = BeautifulSoup(part)
# 	if ("<div") in part:
# 		print part_soup.get_text()
# 		for link in part_soup.find_all('a' , href=True):
# 			link_url = "http://quora.com" + link['href'] + "?share=1"
# 			fw_links.write((link_url + '\n').encode('utf-8'))
# 		count += 1
# print "links read: " + str(count)

# fw_links.close()




###Question 2
fw_topic_names = open("topic_names.txt",  mode='w')
fw_topic_urls = open("topic_urls.txt", mode='w')
fw_topic_names.write((top_level_topic+ '\n').encode('utf-8'))
fw_topic_urls.write((top_level_url + '\n').encode('utf-8'))
#question_2(top_level_url, top_level_topic, top_level_url)
fw_topic_names.close()
fw_topic_urls.close()

##Question3 => Worry: store in global variables =>Run out of memory
#Not sure what we want to do when we extract => store it somewhere, or
#not necessary

#At index 0, for answer_list[0], we will ba able to answer 3-a,b,c,d by
#accessing the first element in other lists.
#answer_list=[] #for a single question
#user_id_list=[] #for a single question
#num_upvote_list=[]
#users_upvote_list=[] #each answer corresponds to an upvote list => list of lists
question_3("http://www.quora.com/U-S-City-Mayors")

browser.close()
