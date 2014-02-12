################################################################
# EE239 PROJECT-1 -  Winter 2014
# Crawling and Data collection on the web

# Students:
# Lauren Samy (304010107)
# Tuan Le (304009873)
# Xiao Li (804126105)

# Chosen Topic:
# Government Leaders and Politicians
# http://www.quora.com/Government-Leaders-and-Politicians
###############################################################


from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import time
import sys
import re
from sets import Set
import os





### Polo Lee
### 02-06-2014
### For Question 1
### Save homepage html file
def question_1():
	global domain
	global browser
	global chosen_topic

	top_level_url = domain + '/' + chosen_topic.replace(" ","-")
	fw = open(chosen_topic.replace(" ","-")+'.html', mode='w')	
	browser.get(top_level_url+'?share=1')
	src_updated = browser.page_source
	src = ""
	while src != src_updated:
		src = src_updated
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(5)
		src_updated = browser.page_source
	html_source = browser.page_source
	pretty_soup = BeautifulSoup(html_source)
	html_source = pretty_soup.prettify()
	fw.write(html_source.encode('utf-8', errors="ignore"))
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
	global browser
	
	about_url = url + '/about?share=1'
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
		fw_topic_names.write((w_topic_name + '\n').encode('utf-8', errors='ignore'))
		topic_url = domain + item['href']
		w_topic_url = w_left_url + '\t' + topic_url
		fw_topic_urls.write((w_topic_url+'\n').encode('utf-8', errors='ignore'))
		question_2_recursive(topic_url, w_topic_name, w_topic_url, fw_topic_names, fw_topic_urls)

### Read the topic_urls.txt
### and give you all the urls
def get_all_topic_urls(filename):
	urls = []
	with open(filename) as fp:
		for line in fp:
			line = line.replace('\n','')
			line = line.split('\t')
			for item in line:
				if item not in urls:
					urls.append(item)
	return urls


def question_2():
	global domain
	global chosen_topic
	global topic_name_file
	global topic_url_file
	top_level_topic = chosen_topic
	top_level_url = domain + '/' + chosen_topic.replace(" ","-")
	fw_topic_names = open(topic_name_file,  mode='w')
	fw_topic_urls = open(topic_url_file, mode='w')
	fw_topic_names.write((top_level_topic+ '\n').encode('utf-8',errors='ignore'))
	fw_topic_urls.write((top_level_url + '\n').encode('utf-8',errors='ignore'))
	question_2_recursive(top_level_url, top_level_topic, top_level_url, fw_topic_names, fw_topic_urls)
	fw_topic_names.close()
	fw_topic_urls.close()







### Tuan Le, Polo
### 02-06-2014
### For Question3

### return {{{...}}}
def collect_list_text(list_text):
	result = ""
	for index in range(len(list_text)):
		result = result + list_text[index]
		if index != len(list_text)-1:
			result = result + ", "
	result = "{{{" + result + "}}}"
	return result

def check_index_range(index, to_check_list):
	if index < len(to_check_list):
		return True
	else:
		return False

def question_3(url, fw_answer_csv):
	global domain
	global browser
	
	pure_topic_url = url
	if url.find("?share=1") == -1:
		url = url + '?share=1'
	
	browser.get(url)
	src_updated = browser.page_source
	src = ""

	#scroll down the page until the end is reached and no more questions
	#are loaded
	while src != src_updated:
		src = src_updated
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(2)
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
	
	#Note that question_dict.keys() or question_dict.values()
	#return list where items appear in random order
	for question in question_list:
		question_text = question.get_text()
		question_url = domain + question['href']
		pure_question_url = question_url


		#debugging purpose
		#print("\n")
		#print("Question text: "+question_text)
		#print("\n")
		#print("Question url: "+question_url)
		
		if question_url.find("?share=1") == -1:
			question_url = question_url + '?share=1'

		#save to dictionary [question_text:question_url]  
		#question_text_url_dict[question_text] = question_url.encode('utf-8')
		# question_url = "http://www.quora.com/Who-is-the-mayor-of-Palo-Alto?share=1"
		browser.get(question_url)
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
						
					answer_text = answer_processed[0].get_text()
					answer_text_list.append(answer_text)
					#save to dictionary [question_text:answer_text_list]
					#question_text_answers_dict[question_text] = answer_text_list

					#debugging
					#print("\n");
					#print("Answer text: "+answer_text.encode('utf-8'))

		#debugging => this #prints very long text
		##print("\nquestion_text_answers_dict\n")
		##print(question_text_answers_dict)

		#Question 3-a
		extracted_user_id_list = []
		answer_user_list = question_soup.find_all(attrs={"class":"answer_user"})
		for answer in answer_user_list:
			#since the person that gives the answer and the voter belong to the same answer sequence,
			#we need to filter out the voters. The person who answers is the one with the first
			#user tag appears in "answer" html sequence
			answer_user = answer.find(attrs={"class":"user"})
			if answer_user is not None:
				user_url = domain + answer_user.get('href')
				extracted_user_id_list.append(user_url)

		#debugging
		#print("\nextracted_user_id_list\n")
		#print(extracted_user_id_list)

		#Question 3-b
		extracted_answer_date_list = []
		answer_date_list = question_soup.find_all(attrs={"class":"answer_permalink"})
		for answer in answer_date_list:
			answer_date = answer.get_text().replace(',','')
			extracted_answer_date_list.append(answer_date)

		#debugging
		#print("\nextracted_answer_date_list\n")
		#print(extracted_answer_date_list)

		#Question 3-c
		extracted_num_upvote_list = []
		num_upvote_list = question_soup.find_all(attrs={"class":"rating_value"})
		for upvote in num_upvote_list:
			num_upvote = upvote.get_text()
			extracted_num_upvote_list.append(num_upvote)

		#debugging
		#print("\nextracted_num_upvote_list\n")
		#print(extracted_num_upvote_list)

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

		#browser.find_element_by_partial_link_text("more").click()
		#will throw NotClickableException if we scroll down the page
		#more_link text must be visible to be clickable. Since we scroll down to the
		#bottom, we have to scroll up again before being able to click the text.
		#CAUTION: Not scroll up, get a WebDriverException at
		#browser.find_element_by_link_text(more_link_text).click()
		# browser.execute_script("window.scrollTo(0, 0);")
		# time.sleep(5) #give enough time to scroll to the top before trying to activate more_link
		
		user_list = question_soup.find_all(attrs={"class":"answer_user"})
		for user in user_list:
			more_link_result = user.find(attrs={"class":"more_link"})
			if more_link_result is not None:
				more_link_text = more_link_result.get_text()
				if check_exists_by_partial_link_text(more_link_text):
					link_object = browser.find_element_by_link_text(more_link_text).click()
					time.sleep(2) #enough time to load content from more_link before activating another link
					

		#load new page source                
		updated_page = browser.page_source
		updated_soup = BeautifulSoup(updated_page)

		all_extracted_answer_voter_list = []
		list_of_answer_voter_list = updated_soup.find_all(attrs={"class":"answer_voters"})
		for element_of_list_of_answer_voter_list in list_of_answer_voter_list:
			extracted_answer_voter_list = [] #answer_voter_list per answer
			answer_voter_list = element_of_list_of_answer_voter_list.find_all(attrs={"class":"user"})
			for answer_voter in answer_voter_list:
				answer_voter_id = domain + answer_voter.get('href')
				extracted_answer_voter_list.append(answer_voter_id)
			all_extracted_answer_voter_list.append(extracted_answer_voter_list)

		#debugging
		#print("\nall_extracted_answer_voter_list\n")
		#print(all_extracted_answer_voter_list)


		### Question 4
		### extracted all the tagged topics : Polo
		all_tagged_topics = question_soup.find_all(attrs={"class":"topic_name"})
		extracted_tagged_topic_list =[]
		for each_tagged_topic in all_tagged_topics:
			each_topic_url = domain + each_tagged_topic.get('href')
			extracted_tagged_topic_list.append(each_topic_url)
		## debugging
		#print("\nextracted_tagged_topic_list\n")
		#print extracted_tagged_topic_list


		## write all the information into answer.csv ; Polo
		question_id = pure_question_url
		topics = collect_list_text(extracted_tagged_topic_list)
		current_topic = pure_topic_url
		left_brace = "{{{"
		right_brace = "}}}"
		comma = ", "
		question_text = left_brace+question_text+right_brace
		for index in range(len(extracted_user_id_list)):
			user_id = extracted_user_id_list[index]
			answer_id = (question_id + "-" + user_id)
			date = ""
			if(check_index_range(index, extracted_answer_date_list)):
				date = extracted_answer_date_list[index]
			number_of_upvotes = "0"
			if(check_index_range(index, extracted_num_upvote_list)):
				number_of_upvotes = extracted_num_upvote_list[index]
			users_who_upvoted = left_brace+""+right_brace
			if(check_index_range(index, all_extracted_answer_voter_list)):
				users_who_upvoted = collect_list_text(all_extracted_answer_voter_list[index])
			answer_text = left_brace + "" + right_brace
			if(check_index_range(index, answer_text_list)):
				answer_text = left_brace+ answer_text_list[index] + right_brace

			line = answer_id + comma + question_id + comma + user_id + comma + date + comma + number_of_upvotes + comma + users_who_upvoted + comma + topics + comma + current_topic + comma + question_text + comma + answer_text + "\n"
			fw_answer_csv.write(line.encode('utf-8','ignore'))



		#TODO: REMOVE THIS LINE
		# time.sleep(1000) #have some time to examine the content manually










### Polo
### 02-09-2014
### For Question 4
def question_4():
	global topic_url_file
	global answer_csv_file
	all_topic_urls = get_all_topic_urls(topic_url_file);
	fw_answer_csv = open(answer_csv_file, mode='w')
	for topic_url in all_topic_urls:
		print topic_url
		question_3(topic_url, fw_answer_csv)
	#debugging
	# question_3("http://www.quora.com/Otis-Rolley-1", fw_answer_csv)
	fw_answer_csv.close()








### Tuan Le, Lauren, Polo
### 02-07-2014
### For Question 5
def question_5_helper(fw_user_csv, user_url):
	global domain
	global browser
	
	pure_user_url = user_url
	if user_url.find("?share=1") == -1:
		user_url = user_url + '?share=1'
	#print user_url
	browser.get(user_url)
	soup = BeautifulSoup(browser.page_source)

	#No need to scroll down since for each of the data we want to extract,
	#we have to open a corresponding link

	user_href = user_url.split("com")[1].split('?')[0] # /Ian-York
	
	# Extract number_of_topics
	topic_href = user_href + "/topics" # /Ian-York/topics
	number_of_topics = "0" 
	topic_href_attr = soup.find(attrs={"href":topic_href})
	if topic_href_attr is not None:
		number_of_topics = topic_href_attr.find(attrs={"class":"light normal profile-tab-count"}).get_text()
	#debugging
	#print("\nnumber_of_topics: " + number_of_topics)

	# QUESTION 5: Extract number_of_blogs
	blog_href = user_href + "/blogs" # /Ian-York/blogs
	number_of_blogs = "0"
	blog_href_attr = soup.find(attrs={"href":blog_href})
	if blog_href_attr is not None:
		number_of_blogs = blog_href_attr.find(attrs={"class":"light normal profile-tab-count"}).get_text()
	#debugging
	#print("\nnumber_of_blogs: " + number_of_blogs)
	
	# QUESTION 5: Extract number_of_questions
	question_href = user_href + "/questions" # /Ian-York/questions
	number_of_questions = "0"
	question_href_attr = soup.find(attrs={"href":question_href})
	if question_href_attr is not None:
		number_of_questions = question_href_attr.find(attrs={"class":"light normal profile-tab-count"}).get_text()
	#debugging
	#print("\nnumber_of_questions: " + number_of_questions)

	# QUESTION 5: Extract number_of_answers
	answer_href = user_href + "/answers" # /Ian-York/answers
	number_of_answers = "0"
	answer_href_attr = soup.find(attrs={"href":answer_href})
	if answer_href_attr is not None:
		number_of_answers = answer_href_attr.find(attrs={"class":"light normal profile-tab-count"}).get_text()
	#debugging
	#print("\nnumber_of_answers: " + number_of_answers)

	# QUESTION 5: Extract number_of_edits
	log_href = user_href + "/log" # /Ian-York/log
	number_of_edits = "0"
	log_href_attr = soup.find(attrs={"href":log_href})
	if log_href_attr is not None:
		number_of_edits = log_href_attr.find(attrs={"class":"light normal profile-tab-count"}).get_text()
	#debugging
	#print("\nnumber_of_edits: " + number_of_edits)

	# QUESTION 5: Extract list of followers (user_ids of these followers)
	follower_url = domain + user_href + "/followers?share=1" # http://www.quora.com/Ian-York/followers?share=1
	browser.get(follower_url)

	src_updated = browser.page_source
	src = ""

	#scroll down the page until the end is reached
	while src != src_updated:
		src = src_updated
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(2) #5s is not enough! Load images is slow
		src_updated = browser.page_source

	soup = BeautifulSoup(src_updated)

	extracted_follower_list = []
	pagedList_item_list = soup.find_all(attrs={"class":"pagedlist_item"})
	for follower in pagedList_item_list:
		user = follower.find(attrs={"class":"user"})
		if user is not None: #Anonymous user doesn't have class attribute user
			follower_url = domain + user.get('href')
			extracted_follower_list.append(follower_url)

	# QUESTION 5: Extract list of following (user_ids of these following)
	following_url = domain + user_href + "/following?share=1" # http://www.quora.com/Ian-York/following?share=1
	browser.get(following_url)

	src_updated = browser.page_source
	src = ""

	#scroll down the page until the end is reached
	while src != src_updated:
		src = src_updated
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(1) #10s is not enough! Load images is slow
		src_updated = browser.page_source

	soup = BeautifulSoup(src_updated)

	extracted_following_list = []
	pagedList_item_list = soup.find_all(attrs={"class":"pagedlist_item"})
	for following in pagedList_item_list:
		user = following.find(attrs={"class":"user"})
		if user is not None: #Anonymous user doesn't have class attribute user
			following_url = domain + user.get('href')
			extracted_following_list.append(following_url)

	
	followers = collect_list_text(extracted_follower_list)
	following = collect_list_text(extracted_following_list)
	comma = ", "

		
	users_line = pure_user_url.decode('utf-8','ignore') + comma + number_of_topics + comma + number_of_blogs + comma + number_of_questions + comma + number_of_answers + comma + number_of_edits + comma + followers + comma + following + "\n"
	fw_user_csv.write(users_line.encode('utf-8', "ignore"))

def process_line_answer(line):
	chunks = line.split('{{{')
	if len(chunks) < 5:
		return []
		

	first_part = chunks[0].split(',')
	if len(first_part) < 5:
		return []
	asnwer_id_field = first_part[0]
	question_id_field = first_part[1]
	user_id_field = first_part[2]
	date_field = first_part[3]
	num_of_upvotes_field = first_part[4]

	users_who_upvoted_field = chunks[1].split("}}}")[0].split(',')
	topics_field = chunks[2].split("}}}")[0].split(',')
	current_topic = chunks[2].split("}}}")[1].replace(',','')
	question_text_field = chunks[3].split('}}}')[0]
	answer_text_field = chunks[4].split("}}}")[0]	

	
	fields = []
	fields.append(asnwer_id_field)
	fields.append(question_id_field)
	fields.append(user_id_field)
	fields.append(date_field)
	fields.append(num_of_upvotes_field)
	fields.append(users_who_upvoted_field)
	fields.append(topics_field)
	fields.append(current_topic)
	fields.append(question_text_field)
	fields.append(answer_text_field)
	
	return fields

def process_line_user(line):
	chunks = line.split("{{{")
	if len(chunks) < 3:
		return []

	first_part = chunks[0].split(',')
	if len(first_part) < 6:
		return []
	user_id_field = first_part[0]
	num_of_topics_field = first_part[1]
	num_of_blogs_field = first_part[2]
	num_of_questions_field = first_part[3]
	num_of_answers_field = first_part[4]
	num_of_edits_field = first_part[5]

	followers_field = chunks[1].split('}}}')[0].split(',')
	following_field = chunks[2].split('}}}')[0].split(',')

	fields = []
	fields.append(user_id_field)
	fields.append(num_of_topics_field)
	fields.append(num_of_blogs_field)
	fields.append(num_of_questions_field)
	fields.append(num_of_answers_field)
	fields.append(num_of_edits_field)
	fields.append(followers_field)
	fields.append(following_field)

	return fields



def question_5():
	global answer_csv_file
	global user_csv_file
	user_url_list = []
	# user_urls = Set()
	
	answers_file = open(answer_csv_file,  mode='r')

	for line in answers_file:
		line_list = process_line_answer(line)
		if len(line_list) != 10:
			continue
		responder = line_list[2]
		if responder not in user_url_list:
			user_url_list.append(responder)
		voters = line_list[5]
		for voter in voters:
			if voter not in user_url_list:
				user_url_list.append(voter)

	answers_file.close()

	users_file = open(user_csv_file, "w")
	for user_url in user_url_list:
		if user_url != "":
			print user_url
			question_5_helper(users_file, user_url)
	users_file.close()
	


### Polo, Lauren
### 02-10-2014
### Question 6

def answer_parser(line_number):
	global answer_csv_file
	count = 0
	chosen_line = ""
	with open(answer_csv_file, mode='r') as fr_csv:
		for line in fr_csv:
			count += 1
			if count == line_number:
				chosen_line = line
	
	fr_csv.close()
	if chosen_line == "":
		print "Line # out of range!!!"
		exit(1)

	return process_line_answer(chosen_line)

def user_parser(line_number):
	global user_csv_file
	count = 0
	chosen_line = ""
	with open(user_csv_file, mode='r') as fr_csv:
		for line in fr_csv:
			count += 1
			if count == line_number:
				chosen_line = line
	
	fr_csv.close()
	if chosen_line == "":
		print "Line # out of range!!!"
		exit(1)

	return process_line_user(chosen_line)

################################################
#~~~~~~~~~~~~~~~~Help Function~~~~~~~~~~~~~~~~~#
################################################
def pretty_html(url, output_file_name):
	global browser
	if "share" not in url:
		url = url+"?share=1"
	browser.get(url)
	
	src_updated = browser.page_source
	src=""
	while src != src_updated:
		time.sleep(1)
		src = src_updated
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		src_updated = browser.page_source

	html_source = browser.page_source
	pretty_soup = BeautifulSoup(html_source)
	pretty_html = pretty_soup.prettify()

	fw_pretty = open(output_file_name, mode='w')
	fw_pretty.write(pretty_html.encode('utf-8'))
	fw_pretty.close()













#########################################
#			main start      #
#########################################
if __name__ == "__main__":
	## CONFIGURE YOUR OWN PATH HERE for chrome driver
	# chromedriver = "C:\\seltests\\virtualenv-1.10.1\\Scripts\\chromedriver.exe"
	# os.environ["webdriver.chrome.driver"] = chromedriver
	# browser = webdriver.Chrome(chromedriver)
	## DEFAULT PATH
	browser = webdriver.Chrome()
	
	domain = 'http://www.quora.com'
	chosen_topic = 'Government Leaders and Politicians'
	topic_name_file = "topic_names.txt"
	topic_url_file = "topic_urls.txt"
	answer_csv_file = "answers.csv"
	user_csv_file = "users.csv"

	print "domain: " + domain
	print "chosen_topic: " + chosen_topic
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

	## test question 1
	# question_1()

	## test question 2
	# question_2()

	## test question 3+4
	# question_4()

	## test question 5
	# question_5()

	## test question 6
	# test_line_number = 5
	# answer_fields = answer_parser(test_line_number)
	# # user_parser(test_line_number)
	# for field in answer_fields:
	# 	print field
	# user_fields = user_parser(test_line_number)
	# for field in user_fields:
	# 	print field

	## test pretty_html
	# pretty_html("http://www.quora.com/Who-are-the-most-embarrassing-politicians-from-your-state", "test.html")

	browser.close()
