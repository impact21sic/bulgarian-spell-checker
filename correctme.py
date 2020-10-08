import re
import requests 
from bs4 import BeautifulSoup
import sys
import os

try:
    word = sys.argv[1]
except IndexError:
    print('Use: python3 correctme.py \'example word\'')
    sys.exit()

url = 'https://rechnik.chitanka.info/w/{}'.format(word)
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

try:
    string = soup.select_one('span[id*=name-stressed]').text 
    answer = "".join(string.split())
except AttributeError:
    pass

all_a = soup.find_all('a')
all_h1 = soup.find_all('h1')
all_h2 = soup.find_all('h2')
all_h3 = soup.find_all('h3')
all_p = soup.find_all('p')
all_span = soup.find_all('span')

if len(all_p) > 1:
    if re.search('>(.*?)<', str(all_p[1])): 
        if re.search('>(.*?)<', str(all_p[1])).group(1) == 'Търсената дума липсва в речника.':
            print('Търсената дума липсва в речника.')
            sys.exit()

    if re.search('> (.*?) <', str(all_p[1])):
        if re.search('> (.*?) <', str(all_p[1])).group(1) == 'е грешно изписване на':
            print('Правилно се изписва {}'.format(re.search('>(.*?)<', str(all_a[9])).group(1)))
            sys.exit()
    
if re.search('\n   (.*?) —', str(all_h2[0])):
    if re.search('\n   (.*?) —', str(all_h2[0])).group(1) == word:
        print('{} е правилно изписана.'.format(word))
        sys.exit()
    
if re.search('>(.*?) <', str(all_h3[0])):
    if re.search('>(.*?) <', str(all_h3[0])).group(1) == 'Значение':
        print('{} е правилно изписана.'.format(answer))
        sys.exit()
