from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import quote_plus
import time
import random
from fake_useragent import UserAgent

app = Flask(__name__)
CORS(app)

# Initialize fake user agent
ua = UserAgent()

def get_headers():
    """Get rotating headers to avoid bot detection"""
    return {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

def search_academic_web(paper_title):
    """Direct web search for academic content using Bing"""
    try:
        # Encode the search query
        query = f'"{paper_title}" (slides OR lecture OR course OR tutorial OR presentation) site:.edu OR site:.ac.uk OR site:.edu.au OR site:slideshare.net OR site:researchgate.net'
        encoded_query = quote_plus(query)
        search_url = f"https://www.bing.com/search?q={encoded_query}"
        
        headers = get_headers()
        
        # Add random delay to avoid rate limiting
        time.sleep(random.uniform(1, 2))
        
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return []
            
        soup = BeautifulSoup(response.content, 'html.parser')
        results = []
        
        # Extract search results from Bing
        result_divs = soup.find_all('li', class_='b_algo')
        
        positive_keywords = [
            'excellent', 'novel', 'breakthrough', 'impressive', 'state-of-the-art',
            'outstanding', 'remarkable', 'innovative', 'pioneering', 'significant',
            '优秀', '创新', '突破', '出色', '先进', '重要意义', '值得借鉴'
        ]
        
        for div in result_divs[:10]:  # Limit to first 10 results
            try:
                title_elem = div.find('h2')
                if title_elem and title_elem.find('a'):
                    title = title_elem.get_text().strip()
                    url = title_elem.find('a').get('href', '')
                    
                    # Get snippet/description
                    desc_elem = div.find('p')
                    snippet = desc_elem.get_text().strip() if desc_elem else ''
                    
                    # Check for positive sentiment
                    text_to_check = f"{title} {snippet}".lower()
                    if any(keyword.lower() in text_to_check for keyword in positive_keywords):
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet,
                            'source': 'web_search'
                        })
                        
            except Exception as e:
                continue
                
        return results
        
    except Exception as e:
        print(f"Error in web search: {e}")
        return []

def search_chinese_web(paper_title):
    """Direct search for Chinese academic content"""
    try:
        # Search Baidu
        query = f'"{paper_title}" (课件 OR 幻灯片 OR 教程 OR 文档)'
        encoded_query = quote_plus(query)
        search_url = f"https://www.baidu.com/s?wd={encoded_query}"
        
        headers = get_headers()
        time.sleep(random.uniform(1, 2))
        
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return []
            
        soup = BeautifulSoup(response.content, 'html.parser')
        results = []
        
        # Extract Baidu search results
        result_divs = soup.find_all('div', class_='result')
        
        positive_keywords = ['优秀', '创新', '突破', '出色', '先进', '重要意义', '值得借鉴']
        
        for div in result_divs[:8]:
            try:
                title_elem = div.find('h3')
                if title_elem and title_elem.find('a'):
                    title = title_elem.get_text().strip()
                    url = title_elem.find('a').get('href', '')
                    
                    # Get description
                    desc_elem = div.find('div', class_='c-abstract')
                    snippet = desc_elem.get_text().strip() if desc_elem else ''
                    
                    # Check for positive keywords
                    if any(keyword in title or keyword in snippet for keyword in positive_keywords):
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet,
                            'source': 'chinese_web'
                        })
                        
            except Exception as e:
                continue
                
        return results
        
    except Exception as e:
        print(f"Error in Chinese web search: {e}")
        return []

def search_semantic_scholar(paper_title):
    """Search Semantic Scholar for citations"""
    try:
        # Search for the paper first
        search_url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={quote_plus(paper_title)}&limit=1"
        response = requests.get(search_url, timeout=10)
        
        if response.status_code != 200:
            return []
            
        data = response.json()
        if not data.get('data'):
            return []
            
        paper_id = data['data'][0]['paperId']
        
        # Get citations for this paper
        citations_url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations?fields=title,abstract,authors,year&limit=10"
        citations_response = requests.get(citations_url, timeout=10)
        
        if citations_response.status_code != 200:
            return []
            
        citations_data = citations_response.json()
        citations = []
        
        # Positive keywords for filtering
        positive_keywords = [
            'excellent', 'novel', 'breakthrough', 'impressive', 'state-of-the-art',
            'outstanding', 'remarkable', 'innovative', 'pioneering', 'significant'
        ]
        
        for citation in citations_data.get('data', []):
            cited_paper = citation.get('citingPaper', {})
            abstract = cited_paper.get('abstract', '').lower()
            title = cited_paper.get('title', '').lower()
            
            # Check if contains positive keywords
            text_to_check = f"{title} {abstract}"
            if any(keyword in text_to_check for keyword in positive_keywords):
                citations.append({
                    'title': cited_paper.get('title', ''),
                    'authors': [author.get('name', '') for author in cited_paper.get('authors', [])],
                    'year': cited_paper.get('year', ''),
                    'abstract': cited_paper.get('abstract', ''),
                    'source': 'academic_paper'
                })
                
        return citations[:5]  # Limit to top 5
        
    except Exception as e:
        print(f"Error in Semantic Scholar search: {e}")
        return []

@app.route('/api/search', methods=['POST'])
def search_citations():
    """Main search endpoint"""
    try:
        data = request.get_json()
        paper_title = data.get('paper_title', '').strip()
        
        if not paper_title:
            return jsonify({'error': 'Paper title is required'}), 400
            
        # Perform all searches
        academic_papers = search_semantic_scholar(paper_title)
        web_results = search_academic_web(paper_title)
        chinese_results = search_chinese_web(paper_title)
        
        result = {
            'academic_papers': academic_papers,
            'web_search_results': web_results,
            'chinese_web_results': chinese_results,
            'total_results': len(academic_papers) + len(web_results) + len(chinese_results)
        }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in search_citations: {e}")
        return jsonify({'error': 'Search failed'}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)