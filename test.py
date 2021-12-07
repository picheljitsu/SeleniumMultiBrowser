import SeleniumMultibrowser
a = SeleniumMultibrowser.SeleniumMultiBrowser(config_file='config.json')
print(a.driver_path)


user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"]#,
    # "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36",
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36",
    # "Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2820.59 Safari/537.36",
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2762.73 Safari/537.36",
    # "Mozilla/5.0 (X11; Linux ppc64le; rv:75.0) Gecko/20100101 Firefox/75.0",
    # "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/75.0",
    # "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:75.0) Gecko/20100101 Firefox/75.0"]

print("[*] Loading User Agents")
a.user_agents = user_agents

print(a.user_agents)
a.get_url(target_url='https://www.linkedin.com')

if a.set_element_id('session_key'):
    print("[*] Got login box.")
    a.send_keys(a.username)

if a.set_element_id('session_password'):
    print("[*] Got password field.")
    a.send_keys("Tdo4tdo4!")

a.login()    
#a.get_url('https://www.linkedin.com/search/results/people/?currentCompany=%5B%221463%22%2C%22676158%22%2C%2213584695%22%2C%229315172%22%2C%2218513542%22%2C%2240690001%22%2C%2240689987%22%5D&origin=COMPANY_PAGE_CANNED_SEARCH')
a.get_elements_class('app-aware-link')
a.set_elements_class('app-aware-link')
a.active_element.get_property('lastElementChild').get_property('innerText')
# spans = a.browsers[0].find_elements_by_tag_name('span')
# for i in range(0, len(spans)):
#     if 'View' in spans[i].text:
#         print("{} {}".format(i, spans[i-1].text))
#a.browsers[0].find_elements_by_class_name('app-aware-link')[1].get_property('lastElementChild').get_property('innerText')