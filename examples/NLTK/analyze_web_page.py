from bs4 import BeautifulSoup
 
import urllib.request
 
response = urllib.request.urlopen('https://es.wikiquote.org/wiki/Agust%C3%ADn_de_Hipona')
 
html = response.read()
 
soup = BeautifulSoup(html,"html5lib")
 
text = soup.get_text(strip=True)
 
print (text)