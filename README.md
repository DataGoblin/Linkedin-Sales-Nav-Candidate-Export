# Intro
Uses the private sales-api to export users into a CSV file. Useful for local CRM's or extra analysis of potential candidates.

**😱Usage can lead to suspension of your Linkedin account.**  | (Please see the disclaimer at the bottom of this page.)

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
	- Employee Count*
	(*) of the company they are working for

 - You can only export 2500 users per search(url). This is a hard limit. However, you can bypass it by setting different filters to split up the totals into multiple URL's. 
 - It is highly recommended to export at MAXIMUM 2500 users per day to limit your chance of having your account suspended. You can increase this amount as you 'warm up' your account with daily exports. 

# Disclaimer Stuff

This code is in no way affiliated with, authorized, maintained, sponsored or endorsed by Linkedin or any of its affiliates or subsidiaries. This is an independent and unofficial project. Use at your own risk.

This project violates Linkedin's User Agreement Section 8.2, and because of this, Linkedin may (and will) temporarily or permantly ban your account. You are responsible for your account being banned if you use this program.

 



