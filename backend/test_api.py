import requests
import json

# Test the backend API
def test_api():
    print("Testing Paper Citation Finder APIs...")
    
    # Test health check
    try:
        health_response = requests.get('http://localhost:5000/health')
        print(f"Health check: {health_response.status_code}")
    except Exception as e:
        print(f"Health check failed: {e}")
    
    # Test search endpoint
    try:
        search_data = {'paper_title': 'attention is all you need'}
        headers = {'Content-Type': 'application/json'}
        search_response = requests.post(
            'http://localhost:5000/api/search',
            json=search_data,
            headers=headers,
            timeout=30
        )
        print(f"Search API Status: {search_response.status_code}")
        if search_response.status_code == 200:
            result = search_response.json()
            print(f"Total results: {result.get('total_results', 0)}")
            print("API working correctly!")
        else:
            print(f"API Error: {search_response.text}")
    except Exception as e:
        print(f"Search API failed: {e}")

if __name__ == "__main__":
    test_api()