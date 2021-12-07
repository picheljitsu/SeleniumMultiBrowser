import os, sys, time
from datetime import datetime
from urllib.parse import urlparse, parse_qs, uses_relative
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as driverwait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By as element_type
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from random import randint
from json import loads

class SeleniumMultiBrowser:

    driver_path = ''
    default_driver_name = 'geckodriver'

    def __init__(self, driver_path='', config_file=''):
        self.target_url = None
        self.last_url = None
        self.driver_path = None
        self.config_file = None
        self.ops_log_path = None
        self.username = None
        self.password = None
        self.active_element_type = None     
        self._active_browser = None
        self._active_element = None
        self.timeout = 4
        self._timeout = None
        self._isterminated = False
        self.target_url = ''
        self.last_error = ''
        self._browsers = []
        self._user_agents = []

        if os.name == 'nt':
            driver = self.default_driver_name + '.exe'
        elif os.name == 'posix':
            driver = self.default_driver_name

        if not driver_path:
            paths = os.environ['PATH'].split(os.pathsep)
            if any([os.path.isfile(os.path.join(i, driver)) for i in paths]):
                pass
            else:
                raise ValueError("Web driver path not found")   

        if config_file:
            self.config_file = config_file           
            configs = self.load_configs(config_file)

            for k in configs.keys():
                if hasattr(self, (k.lower())):
                    self.log_status('[+] Set config -> {} = {}'.format(k.lower(),configs[k]))
                    self.__setattr__(k.lower(), configs[k])
                    
        if driver_path:
            self.driver_path = driver_path

        elif not driver_path and not self.default_driver_name:
            raise ValueError("Web driver path not set or found.") 

    def load_configs(self, config_file):
        if os.path.exists(config_file):
            self.config_file = config_file

        else:
            self.log_status("[-] No config file found")
            return
                
        self.log_status("[+] Config path found at {}".format(self.config_file))

        with open(self.config_file,'rb') as f:
            r = f.read()
            f.close()

        configs = loads(r)
        return configs

    def set_random_active_browser(self, array_element=None):
        idx = randint(0, len(self.browsers) - 1 )
        self.active_browser = self.browsers[idx]

    def login(self):
        self.active_element.submit()
        if self.__is_loaded(self.active_element_name):
            return True
        else:
            return False            

    def clear_cache(self, browser=None):
        if not browser:
            browser = self.active_browser

        browser.delete_all_cookies()
        self.do_sleep(3)
        browser.get("about:blank")

    def launch_browser(self, user_agent=''):
        if user_agent:            
            self.add_user_agent(user_agent)
            self.log_status("[+] Added User Agent to: {}".format(user_agent))
        
        #Create a browser for every user agent in user_agent property
        for i in self._user_agents:
            self.log_status("[*] Creating browser object with User Agent: {}".format(i))
            profile = self.profile({"general.useragent.override": i})                                
            self.add_browser(webdriver.Firefox(firefox_profile=profile,
                                               executable_path=self.driver_path))
        return

    def get_url(self, target_url=''):        
        if not target_url:
            target_url = self.target_url

        if not self.browsers:
            self.log_status("[*] No browsers available. Launching...")
            self.launch_browser()

        self.set_random_active_browser()
        self.last_url = self.active_browser.current_url
        self.active_browser.get(target_url)

        while not self.timedout():
            if self.active_browser.current_url != self.last_url:
                break
            print('waiting {} // {}'.format(self.active_browser.current_url,self.last_url))

    def clear_status(self):
        self.message = ''
        self.last_error = ''

    def get_element_id(self, elementId, browser=None):
        self.clear_status()
        if not browser:
            browser = self.active_browser

        try:
            self.log_status("[+] Successful enumeration for elementId {}".format(elementId))
            return self.active_browser.find_element_by_id(elementId)

        except Exception as err:
            self.last_error = err
            self.log_status("[!] Failed enumeration for elementId {}\n{}".format(elementId, err))
            return None

    def set_element_id(self, elementId, browser=None):
        self.active_element_type = element_type.ID
        self.active_element_name = elementId        
        self.clear_status()

        if not browser:
            browser = self.active_browser

        id = self.get_element_id(elementId=elementId,browser=browser)

        if id:
            self.active_element = id
            self.log_status("[+] Set active element to {}".format(elementId))
            return True

        self.log_status("[!] Failed to set active element {}".format(elementId))

        return None             

    def get_element_name(self, elementName, browser=None):        
        self.clear_status()
        if not browser:
            browser = self.active_browser

        try:
            element_name = self.active_browser.find_element_by_name(elementName)
            self.log_status("[+] Successful enumeration for id {}".format(elementName))
            return element_name

        except:
            self.log_status("[!] Failed enumeration for id {}".format(elementName))
            return False

    def get_elements_class(self, elementName, browser=None):
        self.clear_status()
        if not browser:
            browser = self.active_browser

        try:
            class_name = self.active_browser.find_elements_by_class_name(elementName)
            self.log_status("[+] Successful enumeration for class {}".format(elementName))
            return class_name           
        except:                            
            self.log_status("[!] Failed enumeration for class {}".format(elementName))
            return False

    def set_elements_class(self, elementName, browser=None):
        self.active_element_type = element_type.CLASS_NAME
        self.active_element_name = elementName
        self.clear_status()
        if not browser:
            browser = self.active_browser

        classname = self.get_elements_class(elementName=elementName, browser=browser)
        
        if classname:
            self.active_element = classname
            self.log_status("[+] Successful enumeration for class {}".format(elementName))
            return True                     
        
        self.log_status("[!] Failed enumeration for class {}".format(elementName))
        return False

    def __is_loaded(self, elementName, browser=None):
        if not browser:
            browser = self.active_browser
        i = 0
        while i < 4:
            self.log_status("[*] Awaiting presence of {} {}".format(self.active_element_type,
                                                                    elementName))
            try:                
                element = driverwait(browser, 5).until(
                    EC.presence_of_element_located((self.active_element_type, elementName))
                )
                if element:
                    return element
            except TimeoutException as timeout:
                i += 1
        return False

    def send_keys(self,input_string, browser_index=None):
        if not browser_index:
            self.active_element.send_keys(input_string)
        else:
            try:
                self.browsers[browser_index].send_keys(input_string)

            except Exception as err:
                self.last_error = err
                self.log_status("Failed to send keys to browser {}\n{}".format(browser_index, err))
    
    def close_browser(self, browser=None):
        if not browser:
            browser = self.active_browser
        browser.close()
        self.browsers = self.browsers.remove(browser)

    @property
    def active_element(self):
        return self._active_element

    @active_element.setter
    def active_element(self, dom_object):
        self._active_element = dom_object

    @property
    def active_browser(self):
        return self._active_browser

    @active_browser.setter        
    def active_browser(self, value):
        self._active_browser = value

    @property
    def browsers(self):
        return self._browsers

    @browsers.setter
    def browsers(self,value):
        self._browsers = value

    def add_browser(self,value):
        self.browsers = self.browsers + [value]

    @property
    def user_agents(self):
        for i in self._user_agents:
            print(i)
        return ''

    @user_agents.setter
    def user_agents(self,list_values):
        self._user_agents = list_values

    def terminate(self):
        for b in self.browsers:
            self.close_browser(b)
            self.log_status("[+] Closed browser with session id {}".format(b.session_id))

        self.isterminated = True

    @property
    def isterminated(self):
        return self._isterminated

    @staticmethod
    def profile(params):
        profile = webdriver.FirefoxProfile() 
        for k, v in params.items():
            #print("key: {} // value: {}".format(k,v))
            profile.set_preference(k, v)
        return profile            

    def timedout(self):
        self.do_sleep()

        if not self._timeout:
            self._timeout = self.timeout
            
        elif self._timeout == self.timeout:
            self._timeout = None
            return True      

        self._timeout -= 1
        return False

    @staticmethod
    def do_sleep(interval=1):
        time.sleep(1)

    def log_status(self, message):
        if self.ops_log_path:

            with open(self.ops_log_path, 'a') as logfile:
               logfile.write("{} {}\n".format(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), message))
               logfile.close()

        #Log to std by default
        else:               
            sys.stdout.write("{}\n".format(message))

if __name__ == "__main__":
    pass
