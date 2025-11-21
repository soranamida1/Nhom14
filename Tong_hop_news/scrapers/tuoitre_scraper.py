import requests
import datetime
from bs4 import BeautifulSoup

def get_articles():
    url = "https://tuoitre.vn/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
    }
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = []
    
    
    title_tags = soup.find_all(['h1','h2', 'h3'], class_='box-title-text')
    
    for tag in title_tags[:5]:
        link_tag = tag.find('a')
        if link_tag:
            title = link_tag.get('title') or link_tag.text.strip()
            link = link_tag.get('href')
            
            if link and not link.startswith('http'):
                link = 'https://tuoitre.vn' + link
            
            if title and link:
                content, published_date = get_article_content(link)
                articles.append({
                    'title': title,
                    'link': link,
                    'content': content,
                    'source': 'tuoitre',
                    'published_date': published_date
                })
    
    return articles

def get_article_content(article_url):
    try:
        response = requests.get(article_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        published_date = None
        date_tag = soup.find('div', attrs={'data-role': 'publishdate'})

        if date_tag:
            date_text = date_tag.text.strip()    

            try:
               
               date_time_str = date_text.split('GMT')[0].strip()
               dt_object = datetime.datetime.strptime(date_time_str, '%d/%m/%Y %H:%M')
               published_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')
            except:
                published_date = None
        
        content_div = soup.find('div', class_='detail-content') or \
                      soup.find('div', class_='detail-cmain')
                      
        content = content_div.get_text(separator='\n', strip=True)if content_div else "Không có nội dung"
        return content, published_date
    except:
        return "Lỗi khi lấy nội dung", None