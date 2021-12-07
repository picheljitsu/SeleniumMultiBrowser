import SeleniumMultiBrowser
a = SeleniumMultiBrowser.SeleniumMultiBrowser(config_file='config.json')
print(a.driver_path)

#Specifies a list of user-agents to use.  Caution on having too many variances of browsers.  Remote
#web servers may render web content different based on the User-Agent, which could break searching/
#scraping and require a seperate parsing logic for each browser type.
user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2820.59 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2762.73 Safari/537.36",
    "Mozilla/5.0 (X11; Linux ppc64le; rv:75.0) Gecko/20100101 Firefox/75.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/75.0",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:75.0) Gecko/20100101 Firefox/75.0"]

print("[*] Loading User Agents")
a.user_agents = user_agents

#Set the user_agents property of the class instance
print(a.user_agents)

#This will automatically launch a browser for each of the user-agents specified
a.get_url(target_url='https://www.linkedin.com')


#The class will randomly select a new browser for each .get_url() method call
#that browser will be set as the class instances a.active_browser property
#So each .get_url() call will automatically rotate the active browser.
if a.set_element_id('session_key'):
    print("[*] Got login box.")
    a.send_keys(a.username)

if a.set_element_id('session_password'):
    print("[*] Got password field.")
    pw = input("Enter you LinkedIn password: ")
    a.send_keys(pw)

if not a.login():
    print("[-] Failed to login.")
    exit()
    
#This URL returns a list of all Microsoft employees.  
a.get_url('https://www.linkedin.com/search/results/people/?currentCompany=%5B%221035%22%2C%2210073178%22%2C%223238203%22%2C%223178875%22%2C%221418841%22%2C%2219537%22%2C%223290211%22%2C%2218612750%22%2C%2211206713%22%2C%221148098%22%2C%221889423%22%2C%22164951%22%2C%223641570%22%2C%22165397%22%2C%225097047%22%2C%221386954%22%2C%22263515%22%2C%2210957831%22%2C%22589037%22%2C%22692068%22%2C%222270931%22%2C%223763403%22%2C%2230203%22%2C%222446424%22%2C%2218086638%22%5D&origin=COMPANY_PAGE_CANNED_SEARCH')

#This code is incomplete, but you could essesntially parse the pages for the names
a.get_elements_class('app-aware-link')
a.set_elements_class('app-aware-link')
listobjects = a.active_element
for obj in listobjects:
    print(obj.get_property('lastElementChild').get_property('innerText'))

