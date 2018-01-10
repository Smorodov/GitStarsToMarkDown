import logging

from grab import Grab

import re   

def is_number_regex(s):
    """ Returns True is string is a number. """
    if re.match("^\d+?\.\d+?$", s) is None:
        return s.isdigit()
    return True

logging.basicConfig(level=logging.DEBUG)

g = Grab()

your_login='your login'
your_password='your password'

g.go('https://github.com/login')
g.doc.set_input('login', your_login)
g.doc.set_input('password', your_password)
g.doc.submit()

repo_url = 'https://github.com/'+your_login + '?tab=stars'

g.go(repo_url)
g.doc.save('x.html')

max_page=0
for elem in g.doc.select('//div[@class="paginate-container"]/div/a'):
    text=elem.text()
    if(is_number_regex(text)):
        pag_num=int(text)
        if(max_page<pag_num):
            max_page=pag_num

print('---------------------------------------------------')
print('Found '+str(max_page)+' pages.')
print('---------------------------------------------------')

text_file = open("MyStars.md", "w")

text_file.write("# My stars #\n")
for current_page in range(1,max_page+1) :
    repo_url = 'https://github.com/'+your_login + '?page='+str(current_page)+'&tab=stars'
    print('---------------------------------------------------')
    print('Processing '+str(current_page)+' page.')
    print('---------------------------------------------------')    
    g.go(repo_url)
    
    for elem in g.doc.select('//div[@class="d-inline-block mb-1"]/h3/a'):
        text_file.write("- [{1}](\"{0}\")\n".format(g.make_url_absolute(elem.attr('href')),elem.text()))
        
text_file.close()