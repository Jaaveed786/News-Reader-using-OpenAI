import requests

def fetch_news(api_key):
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey=b32018f10dcb4036b43864df540c7119"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles')
        if articles:
            for idx, article in enumerate(articles, start=1):
                print(f"{idx}. {article['title']}")
                print(f"   {article['description']}")
                print(f"   Read more: {article['url']}")
                print()
        else:
            print("No articles found.")
    else:
        print("Failed to fetch news.")

def main():
    api_key = 'YOUR_NEWS_API_KEY'  
    fetch_news(api_key)

if __name__ == "__main__":
    main()
