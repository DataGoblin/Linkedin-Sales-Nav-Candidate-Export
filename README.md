# Intro
Uses the private sales-api to export users into a CSV file. Useful for local CRM's or extra analysis of potential candidates.

**😱Usage can lead to suspension of your Linkedin account**

# How to use

**1.** Install the packages this program depends on

    pip install -r requirements.txt
    
	// If you need extra help on this (https://www.youtube.com/watch?v=mBcmdcmZXJg)

Special thanks to package creators, contributors and maintainers!

 - https://github.com/pandas-dev/pandas
 - https://github.com/jfilter/clean-text 
 - https://github.com/psf/requests


**2.** In the file `main.py` there are three fields that need to be filled. These are cookie values from Linkedin.

 - li_at
 - li_a
 - jsessionid

Use the below extension to easily access all of these cookies which you can paste directly into the file
(https://chrome.google.com/webstore/detail/cookiemanager-cookie-edit/hdhngoamekjhmnpenphenpaiindoinpo)

**3.** Now you can do `python main.py` in your terminal to run the program. 

You will be prompted for a URL. Go setup your search on sales-nav with your filters/keywords etc and then simply copy the URL and paste into the program. 

# Extra Information

 - If it was not evident. You will need a sales navigator license for your Linkedin account.
 - A list of fields exported
	- Full Name
	- Current Job Title
	- Current Company
	- Current Industry*
	- Tenure
	- Location
	- Linkedin Profile URL
	- Linkedin Company URL
	- Company URL
	- Company URL
	- Employee Count*
	(*) of the company they are working for

 - You can only export 2500 users per search(url). This is a hard limit. However, you can bypass it by setting different filters to split up the totals into multiple URL's. 
 - It is highly recommended to export at MAXIMUM 2500 users per day to limit your chance of having your account suspended. You can increase this amount as you 'warm up' your account with daily exports. 

# Disclaimer Stuff

This is for (Educational purposes)! 

**⚠️Can I get banned for using this?⚠️**

*Yes! Scraping Linkedin.com is against their [User Agreement](https://www.linkedin.com/help/linkedin/answer/56347/prohibited-software-and-extensions?src=direct/none&veh=direct/none). They have automated scraping detection so if you do take the risk to use this program then I recommend taking it slow and limit your scraping.*

 



