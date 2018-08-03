from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unicodecsv as csv
import random
import sys
import re
driver = webdriver.Chrome()




def page_count_no():
	d=driver.find_element_by_css_selector(".search-pagination-top.clearfix.mtop")
	s=d.text
	r=s.split("of")
	f=r[1].split("\n")
	g=str(f[0])
	return int(g)
	time.sleep(5)


def get_areas():
	driver.get("https://www.zomato.com/ncr")

	areas_file = open("areas.txt","r+")
	fieldnames = ["Area Name","Count"]
	area_data_file = open("area_data.csv","r+")
	csv_writer = csv.DictWriter(area_data_file,encoding = "utf-8",fieldnames = fieldnames)
	
	
	existing_areas_n = areas_file.readlines()				#EXISTING AREA LINKS WITH \N
	
	existing_areas = []
	
	for links in existing_areas_n:
		existing_areas.append(links.strip("\n"))		#EXISTING AREA LINKS WITHOUT \N
		areas_file.close()
		areas_file = open("areas.txt","a+")

	print existing_areas, "\n\nprinted existing areas"	
	#location_box = driver.find_element_by_css_selector(".ui.segment.row")
	location = driver.find_element_by_css_selector(".ui.segment.row")
	location_ele = location.find_elements_by_css_selector("a")
	location_links = []
	#TO BE USED;
	

	for loc in location_ele:

		link = str(loc.get_attribute("href"))
		area_name_un = loc.text
		name_split = area_name_un.split("(")
		area_name = area_name_un.split("(")[0]
		#area_name = str(name_split[0]
		if len(name_split)<=2:
			count_un = name_split[1].split(" places")
			count  = int(count_un[0])
		else:
			count_un = name_split[2]
			count = count_un.split(" ")[0]
		
		area_dict = {"Area Name":area_name,"Count":count}
		
		if link not in existing_areas:
			areas_file.write(link+"\n")
			existing_areas.append(link)
			#csv_writer.writerow(area_dict)
			print "saving link     ",link 


	areas_file.close()	
	area_data_file.close()
	print"get areas sleeping"
	#time.sleep(random.uniform(5.0,30))
	return existing_areas


def get_areas_restaurants(existing_areas): # loads a area's restaurants
	rest_file = open("restaurants.txt","r+")
	links_un = rest_file.readlines()
	rest_file.close()
	links=[]
	for x in links_un:
		links.append(x.strip("\n"))				#LINKS WITHOUT \N
	
	#loaded_file = open("restaurants_loaded.txt","r+")
	#loaded_links = loaded_file.readlines()
	#loaded_file.close()


	done_areas_file = open("areas_done.txt","r+")
	done_areas_un= done_areas_file.readlines()
	done_areas = []
	done_areas_file.close()

	for x in done_areas_un:
		done_areas.append(x.strip("\n"))		#LINKS WITHOUT \N

	done_areas_file = open("areas_done.txt","a+")

	existing_areas = list(set(set(existing_areas)-set(done_areas)))
	print "existing_areas \n\n\n",existing_areas
	rest_file = open("restaurants.txt","a+")
	rest_links = []
	rest_links_un = rest_file.readlines()
	for link in rest_links_un:
		rest_links.append(link.strip("\n"))

	"got restaurant links from file"	
	#loaded_file = open("restaurants_loaded.txt","a+")
	


	#links_count = len(existing_areas)
	#x=0
	print "\n\n\n*************GETTING RESTAURANTS LINKS*********************"
	for area in existing_areas:
		print "\n\n\n"+area+"?all=1"
		driver.get(area + "?all=1"+"&sort=recent")
		load_count = page_count_no()
		time.sleep(random.uniform(2,5))
		#new_to_old_ele=driver.find_elements_by_css_selector(".search_filter.sort.cursor-pointer")
		#new_to_old_ele[4].click()
		for w in range(1,load_count+1):

			driver.get(area+"?all=1&page=%s"%(w)+"&sort=recent")
			#loaded_file.write("Area: "+ area[x] + "Page No: "+w)

			
			rest_ele = driver.find_elements_by_css_selector(".result-title.hover_feedback.zred.bold.ln24.fontsize0 ") #conatins all restaurant links		
			
			

			for x in range(0,len(rest_ele)):
				d = rest_ele[x].get_attribute("href")
				if d in rest_links or d in links:
					print "restaurant link already in file"
					continue
				rest_links.append(str(d))
				rest_file.write(d+"\n")
				print "link written in file",d
				rest_file.flush()
			

			time.sleep(random.uniform(2,5.00))	
		#x+=1
		#x= max(x,links_count)
		#rest_file.write("\n\n\n","%s AREA COMPLETE" %(area), "\n\n\n")
		#rest_file.flush()

		done_areas_file.write(area+"\n")
		done_areas_file.flush()
		print "********CHANGING LOCATION********",area
	rest_file.close()	
	#loaded_file.close()	
	#done_rest_file.close()
	done_areas_file.close()
	return rest_links			




def get_rest_details(all_rest_links_un):
	print "starting rest details**************"
	all_rest_links=[]
	rest_done_file= open("restaurants_done.txt","r+")
	rest_done_un= rest_done_file.readlines()
	rest_done = []

	fieldnames = ["Name","Area","Phone Number","Cost For Two","Rating","Address","Part Of City","Type","Search Keywords","Reviews Count","Claimed Listing","Loved Food","More Info"]
	
	for link in rest_done_un:
		s=link.strip("\n")
		rest_done.append(s)

	for link in all_rest_links_un:
		all_rest_links.append(link.strip("\n"))
	rest_done_file.close()
	rest_done_file= open("restaurants_done.txt","a+")

	print all_rest_links[0:10]
	print "RESTAURANTS DONE \n\n",rest_done[0:10]
	time.sleep(5)
	rest_links = list(set(all_rest_links) - set(rest_done))
	print "FINAL REST LINKS \n\n" ,rest_links[0:10]
	#sys.exit(0)

	rest_data_file = open("restaurants_data.csv","a+")
	csv_writer = csv.DictWriter(rest_data_file,encoding="utf-8",fieldnames=fieldnames)
	rest_error_file = open("restaurants_error.txt","a+")

	# time.sleep(60)

	for link in rest_links:
		
		
		for i in range(2):

			try:		
				driver.get(link)
				if (len(driver.find_elements_by_css_selector(".closed-label.tooltip_formatted.ui.big.red.label.ml0")))!=0:
					print "CLOSED RESTAURANT BREAK"
					break
				
				# try:
				# 	driver.find_element_by_css_selector(".closed-label.tooltip_formatted.ui.big.red.label.ml0").text
				# 	break
				# except:
				# 	pass		

				rest_name = str((driver.find_elements_by_css_selector(".ui.large.header.left"))[0].text)
				print "NAME: ",rest_name,"\n"
				

				rest_area = str(driver.find_elements_by_css_selector(".left.grey-text.fontsize3")[0].text)
				print "AREA: ",rest_area,"\n"
				
				try:
					rest_type_encoded = ((driver.find_elements_by_css_selector(".grey-text.fontsize3"))[1].text).encode("utf-8")
					rest_type_decoded = rest_type_encoded.decode("utf-8")
					rest_type = rest_type_decoded.encode("ascii","ignore")

					if "caf" in rest_type:
						rest_type = rest_type+"e"
					print "TYPE:",rest_type,"\n"
				except:
					rest_type = "Maybe Delivery"					



				try:
					rest_add = str(driver.find_elements_by_css_selector(".resinfo-icon")[0].text)
					print "ADDRESS: ",rest_add,"\n"
				
				except:
					rest_add = driver.find_elements_by_class_name("medium")[1].text
					print "ADDRESS: ",rest_add,"\n"



					
				rest_phno = driver.find_elements_by_css_selector(".fontsize2.bold.zgreen")[0].text
				print "PHONE NO: ",rest_phno,"\n"


				search_keywords = unicode(driver.find_element_by_css_selector(".userKeywords").text).encode("utf-8")
				print "SEARCH KEYWORDS: ",search_keywords,"\n"

				try:

					reviews_text = driver.find_element_by_css_selector(".item.default-section-title.everyone.active.selected").text
					reviews_count = int("".join(re.findall(r'\d+',reviews_text)))
					print "REVIEWS COUNT: ", reviews_count,"\n"

				except:
					reviews_count = 0


				print "REVIEWS COUNT: ",reviews_count,"\n"

				claim_listing = driver.find_element_by_css_selector(".res-header-claims.mbot0.ptop0").text.split("\n")[1]

				try:
					more_info = (", ".join(driver.find_element_by_css_selector(".res-info-highlights").text.split("\n")[1:]))

				except:
					more_info = "Not Available"	

				print "MORE INFO: ",more_info,"\n"
					
				try:
					loved_food = driver.find_element_by_css_selector(".fontsize13.ln18").text

				except:
					loved_food = "Not Available"	
				print "PEOPLE'S LOVED FOOD",loved_food,"\n"

				try:
					cost_for_two = int(driver.find_element_by_xpath("//div[1]/div/div[1]/div[3]/div[1]/div[1]/div[3]/div/div/span[2]").text.split(" for")[0].encode("ascii","ignore").replace(",",""))
				
							
				except:
					try:
						cost_for_two = int(driver.find_element_by_xpath("//div[1]/div/div[1]/div[4]/div[1]/div[1]/div[3]/div/div/span[2]").text.split(" for")[0].encode("ascii","ignore").replace(",",""))
				
					except:
						try:
							cost_for_two = int(driver.find_element_by_xpath("//div[1]/div/div[1]/div[3]/div[1]/div[1]/div[3]/div/div/span[2]").text.split(" for")[0].encode("ascii","ignore").replace(",",""))
						except:
							pass
				print "Cost for Two: ",cost_for_two,"\n"
				try:
					part_of_city = str(driver.find_element_by_xpath("//div/div/div/div/ol/li[4]/span/a/span").text)
				except:
					part_of_city = "Zomato Delivery"	
				print "Part of City: ",part_of_city,"\n"
				
				try:
					rating = driver.find_elements_by_xpath("//div[1]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div")[1].text
				except:
					rating = "Not Available"	
				print "Rating: ",rating,"\n"

				print "x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x"	
				try:
					driver.find_element_by_css_selector(".opening-soon-label.res-notification-label.ui.big.yellow.label.ml0")
					mail_body ="\n\n\n"+"Name: "+rest_name+"\n"+"Area: "+rest_area+"\n"+"Type: "+rest_type.encode('latin-1').decode('utf-8')+"\n"+"Address: "+rest_add+"\n"+"Phone Number: "+rest_phno+"\n"+"Zomato Link: "+link
					import smtplib

					try:  
					    server = smtplib.SMTP('smtp.gmail.com', 587)
					    server.ehlo()
					except:  
					    print 'Something went wrong...'

					fromaddr = 'automationbots2121@gmail.com'
					toaddrs  = 'hardik.squarefork@gmail.com'
					msg = mail_body
					username = 'automationbots2121@gmail.com'
					password = 'blahblahpassword'
					server = smtplib.SMTP('smtp.gmail.com:587')
					server.starttls()
					server.login(username,password)
					server.sendmail(fromaddr, toaddrs, msg)
					server.quit()	

					print "MAIL SENT"
				except: 
					pass	
		
				# try:
				# 	more_locations = driver.find_element_by_css_selector(".clearfix.res-main-address-links").text.encode("ascii","ignore")

				# except:
				# 	more_locations = 
				rest_data_dict = {"Name" : rest_name, "Area" : rest_area, "Phone Number" : rest_phno ,"Cost For Two" : cost_for_two,"Rating": rating, "Address" : rest_add ,"Part Of City": part_of_city,"Type" : rest_type,"Search Keywords" : search_keywords,"Reviews Count" : reviews_count,"Claimed Listing" : claim_listing,"Loved Food" : loved_food,"More Info" : more_info}
				csv_writer.writerow(rest_data_dict) 
				rest_data_file.flush()

				rest_done_file.write(link+"\n")
				rest_done_file.flush()
				print "BREAKING","\n\n\n\n"
				time.sleep(2)
				break
				
			
			except:
				print "ERROR ENCOUNTERED"
				# if i == 4:
				# 	yes_or_no = raw_input("Do you want to continue?\nMade 4 attempts (y/n/s): ")
				# 	if yes_or_no =="y" or yes_or_no =="Y":
				# 		i=i-1	
				# 	elif yes_or_no =="s" or yes_or_no=="S" or yes_or_no =="n" or yes_or_no=="N":
				# 		rest_error_file.write(link+"\n")		
				#else:
				if i==1:
						rest_error_file.write(link+"\n")
						rest_error_file.flush()
						print "Saved error link"
						
				time.sleep(i*2)
				pass		

	rest_done_file.close()
	rest_data_file.close()
	rest_error_file.close()



existing_areas = get_areas()				#PUTS AREA LINKS TO EXISTING AREAS
all_rest_links_un = get_areas_restaurants(existing_areas)		#PUTS ALL RESTAURANTS LINK IN REST LINKS
get_rest_details(all_rest_links_un)