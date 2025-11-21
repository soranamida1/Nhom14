import requests
import datetime
from bs4 import BeautifulSoup

def get_articles():
    url = "https://vnexpress.net/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
    }
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = []
    
    title_tags = soup.find_all(['h1','h2', 'h3'], class_=lambda x: x and 'title' in x)
    
    for tag in title_tags[:5]: 
        link_tag = tag.find('a')
        if link_tag:
            title = link_tag.get('title') or link_tag.text.strip()
            link = link_tag.get('href')
            
            if link and not link.startswith('http'):
                link = 'https://vnexpress.net' + link
            
            if title and link:
                content, published_date = get_article_content(link)
                articles.append({
                    'title': title,
                    'link': link,
                    'content': content,
                    'source': 'vnexpress',
                    'published_date': published_date
                })
    
    return articles
def get_article_content(article_url):
    try:
        response = requests.get(article_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        published_date = None
        date_tag = soup.find('span', class_='date')
        
        if date_tag:
            date_text = date_tag.text.strip() 
            
            try:
                parts = date_text.split(', ')
                
                date_time_str = f"{parts[1]}, {parts[2].split(' (')[0]}"
                
                dt_object = datetime.datetime.strptime(date_time_str, '%d/%m/%Y, %H:%M')
                published_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                    
            except :
               
                published_date = None
        
        content_div = soup.find('article', class_='fck_detail')
        
        if not content_div:
            content_div = soup.find('div', class_='fck_detail')
        
        content = content_div.get_text(separator='\n', strip=True)if content_div else "Không có nội dung"
        return content, published_date
            
    except Exception as e:

        return "Lỗi khi lấy nội dung", None
