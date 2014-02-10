from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
import re




def Question2(link_about,a,b):
        browser.get(link_about)
        html_source=browser.page_source
        soup=BeautifulSoup(html_source)
        list_about_items=soup.find_all(attrs={"class":"topic_name"})
        split_html = html_source.split("<span")
        split_html_strong=html_source.split("<strong")
        for i in range(1,len(split_html_strong)):
                part2=split_html_strong[i].split('</strong>')[0]
                print "part2----------------"
                print part2
                part2_soup=BeautifulSoup(part2)

                if 'Child' in part2_soup.get_text():

                        html_2=split_html_strong[i].split('<span')
                        for i in range(1,len(html_2)):
                                part = html_2[i].split('</span>')[0]
                                part_soup=BeautifulSoup(part)
                                if ("<div") in part:
                                        for link in part_soup.find_all('a',href=True):
                                               # print link['href']
                                               if (link != None):
                                                        link_about="http://quora.com"+link['href']+ "/about"
                                                        string_name=link['href'].strip('/')
                                                        fw_topics.write((a+'\t'+string_name+'\n').encode('utf-8'))
                                                        fw_urls.write((b+'\t'+"http://quora.com"+link['href']+'\n').encode('utf-8'))
                                                        Question2(link_about,a+'\t'+ string_name,b+'\t'+"http://quora.com"+link['href'])
 
                        
                        


###Question 1


url = 'http://www.quora.com/Radical-Politics?share=1'

fw = open("Radical_source.html" , mode='w')
links_file_name = url[21:].split('?')[0]
fw_links = open("Radical_link.txt", mode='w')

#chromedriver = "/Users/farnoosh/Documents/UCLA/UCLA winter 2014/chromedriver"
#os.environ["webdriver.chrome.driver"] = chromedriver
#browser = webdriver.Chrome(chromedriver)
browser = webdriver.Chrome()
browser.get(url)

src_updated = browser.page_source
src = ""
while src != src_updated:
        time.sleep(1)
        src = src_updated
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        src_updated = browser.page_source

html_source = browser.page_source
fw.write(html_source.encode('utf8'))
fw.close()

soup = BeautifulSoup(html_source)
question_links = soup.find_all("h3")
#list_bitems = soup.find_all(attrs={"class":"pagedlist_item"})
#print list_bitems

split_html = html_source.split("<h3>")
count = 0
for i in range(1,len(split_html)):
        part = split_html[i].split('</h3>')[0]
        part_soup = BeautifulSoup(part)
        if ("<div") in part:
                #print part_soup.get_text()
                for link in part_soup.find_all('a' , href=True):
                        link_url = "http://quora.com" + link['href'] + "?share=1"
                        fw_links.write((link_url + '\n').encode('utf-8'))
                count += 1
# print "links read: " + str(count)
global link_about
#link_about='http://www.quora.com/Politics/about'
Link_about1='http://www.quora.com/Radical Politics/about'
Link_about2='http://www.quora.com/Lobbying/about'
Link_about3='http://www.quora.com/Political Careers/about'
global fw_topics
fw_topics = open("topic_names.txt" , mode='w')
fw_urls= open("topic_urls.txt" , mode='w')
#Question2(link_about,None)
fw_topics.write(("Radical Politics"+'\n').encode('utf-8'))
fw_urls.write(("http://www.quora.com/Radical Politics"+'\n').encode('utf-8'))
Question2(Link_about1,"Radical Politics","http://www.quora.com/Radical Politics")


fw_topics.write(("Lobbying"+'\n').encode('utf-8'))
fw_urls.write(("http://www.quora.com/Lobbying"+'\n').encode('utf-8'))
Question2(Link_about2,"Lobbying","http://www.quora.com/Lobbying")

fw_urls.write(("http://www.quora.com/Political Careers"+'\n').encode('utf-8'))
fw_topics.write(("Political Careers"+'\n').encode('utf-8'))
Question2(Link_about3,"Political Careers","http://www.quora.com/Political Careers")
fw_topics.close()
fw_urls.close()
browser.close()




