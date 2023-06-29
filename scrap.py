import requests
from bs4 import BeautifulSoup
import os
archive_base_url = "https://csrc.nist.gov/publications/search?sortBy-lg=relevance&viewMode-lg=brief&ipp-lg=25&status-lg=Final&series-lg=FIPS%2cSP%2cNISTIR%2cITL+Bulletin%2cWhite+Paper%2cBuilding+Block%2cUse+Case%2cJournal+Article%2cConference+Paper%2cBook&topicsMatch-lg=ANY&controlsMatch-lg=ANY&page="

def get_pdf_links(page_url):
    r = requests.get(page_url)
    soup = BeautifulSoup(r.text,'html.parser')
    links = soup.findAll('a')
    pdfs_on_page = [item['href'] for item in soup.select('[href$=".pdf"]')]
    return pdfs_on_page

def download_files(link):
    
    try:
        
        path,file_= os.path.split(link)
   ##print(path)
    
        if not os.path.exists('outputs/'+path):
            os.makedirs('outputs/'+path)
        if os.path.exists('outputs/'+file_):
            print("File Already Exists " + file_)
            return
        else:
            r = requests.get(link)
            with open('outputs/'+file_, 'wb') as f:
                f.write(r.content)
    except requests.exceptions.MissingSchema:
        print(link + " is an invalid schema")
        print("Retrying with updated url... https://csrc.nist.gov"+link)
        download_files("https://csrc.nist.gov"+link)
    except requests.exceptions.ConnectionError:
        print("Unable to connect to: " + link)
    


if __name__ == "__main__":
    all_pdfs = []
    for i in range(1,51):
        url = archive_base_url + str(i)
        links = get_pdf_links(url)
        for link in links:
            all_pdfs.append(link)
    #print(all_pdfs)
    for pdf in all_pdfs:
        download_files(pdf)
    
    
    
    