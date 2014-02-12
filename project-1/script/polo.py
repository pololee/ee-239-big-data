from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import time
import os
import re
from sets import Set

### Polo Lee
### 02-06-2014
### For Question 1
### Save homepage html file
def question_1(domain, chosen_topic):
	top_level_url = domain + '/' + chosen_topic.replace(" ","-")
	fw = open(chosen_topic.replace(" ","-")+'.html', mode='w')
	global browser
	browser.get(top_level_url+'?share=1')
	src_updated = browser.page_source
	src = ""
	while src != src_updated:
		time.sleep(5)
		src = src_updated
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		src_updated = browser.page_source
	html_source = browser.page_source
	pretty_soup = BeautifulSoup(html_source)
	html_source = pretty_soup.prettify()
	fw.write(html_source.encode('utf-8'))
	fw.close()


### Polo Lee
### 02-05-2014
### For Question 2
### Basic idea: use recursive function to make a DFS (Depth First Search)
def check_exists_by_partial_link_text(text):
    try:
        browser.find_element_by_partial_link_text(text)
    except NoSuchElementException:
        return False
    return True

def question_2_recursive(url, w_left_name, w_left_url, fw_topic_names, fw_topic_urls):
	about_url = url + '/about?share=1'
	global browser
	browser.get(about_url)
	if check_exists_by_partial_link_text('View'):
		try:
			browser.find_element_by_partial_link_text('View').click()
		except WebDriverException:
			return
	time.sleep(2)
	about_source = browser.page_source
	about_source = about_source.split('Child Topics')
	if len(about_source) < 2:
		return
	else:
		about_source = about_source[1]
	soup_about = BeautifulSoup(about_source)
	topic_name_list = soup_about.find_all(attrs={"class":"topic_name"})
	for item in topic_name_list:
		w_topic_name = w_left_name + '\t' + item.get_text()
		fw_topic_names.write((w_topic_name + '\n').encode('utf-8'))
		topic_url = domain + item['href']
		w_topic_url = w_left_url + '\t' + topic_url
		fw_topic_urls.write((w_topic_url+'\n').encode('utf-8'))
		question_2_recursive(topic_url, w_topic_name, w_topic_url, fw_topic_names, fw_topic_urls)

### Read the topic_urls.txt
### and give you all the urls
def get_all_topic_urls(filename):
	urls = Set()
	with open(filename) as fp:
		for line in fp:
			line = line.replace('\n','')
			line = line.split('\t')
			for item in line:
				if item not in urls:
					urls.add(item)
	return urls


def question_2(domain, chosen_topic):
	top_level_topic = chosen_topic
	top_level_url = domain + '/' + chosen_topic.replace(" ","-")
	fw_topic_names = open("topic_names.txt",  mode='w')
	fw_topic_urls = open("topic_urls.txt", mode='w')
	fw_topic_names.write((top_level_topic+ '\n').encode('utf-8'))
	fw_topic_urls.write((top_level_url + '\n').encode('utf-8'))
	question_2_recursive(top_level_url, top_level_topic, top_level_url, fw_topic_names, fw_topic_urls)
	fw_topic_names.close()
	fw_topic_urls.close()


### Tuan Le
### 02-06-2014
### For Question3
def question_3(url):
	global browser
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



#########################################
#			main start					#
#########################################
if __name__ == "__main__":
	browser = webdriver.Chrome()
	domain = 'http://www.quora.com'
	chosen_topic = 'Government Leaders and Politicians'
	# question_1(domain, chosen_topic)
	question_2(domain, chosen_topic)
	browser.close()
