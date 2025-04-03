import openai
import requests
from bs4 import BeautifulSoup


def search_google(query):
    url = f"https://www.google.com/search?q={query}&tbm=nws"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        news_results = soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd')
        for idx, result in enumerate(news_results, start=1):
            print(f"{idx}. {result.text}")
    else:
        print("Failed to fetch news.")


def main():
    openai.api_key = 'YOUR_OPENAI_API_KEY'  # Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
    query_prompt = "Get today's news updates from Google."
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=query_prompt,
        max_tokens=50
    )
    query = response.choices[0].text.strip()
    print("Generated Query:", query)
    search_google(query)


if __name__ == "__main__":
    main()
