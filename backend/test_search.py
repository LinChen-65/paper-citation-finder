#!/usr/bin/env python3
"""
Test direct web search functionality
"""

import requests
from fake_useragent import UserAgent
from urllib.parse import quote_plus
import time
import random

def test_direct_search(query):
    """Test direct web search with better headers"""
    try:
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Test with Bing (less restrictive than Google)
        search_url = f"https://www.bing.com/search?q={quote_plus(query)}+site:.edu+OR+site:slideshare.net"
        
        print(f"Searching: {search_url}")
        response = requests.get(search_url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response length: {len(response.text)}")
        
        if response.status_code == 200:
            # Look for academic content indicators
            content = response.text.lower()
            academic_indicators = ['lecture', 'slides', 'course', 'tutorial', 'pdf', 'presentation']
            found_indicators = [ind for ind in academic_indicators if ind in content]
            print(f"Found academic indicators: {found_indicators}")
            
            return len(found_indicators) > 0
            
        return False
        
    except Exception as e:
        print(f"Search error: {e}")
        return False

if __name__ == "__main__":
    test_direct_search("attention is all you need")