import requests
import socket
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

# Use your own API key from https://newsapi.org
API_KEY = "b32018f10dcb4036b43864df540c7119"


def check_internet():
    """Checks if the device is connected to the internet."""
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False


class NewsApp(App):
    def fetch_news(self):
        """Fetches top news headlines from NewsAPI if internet is available."""
        if not check_internet():
            print("No internet connection!")
            return "no_internet"

        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
        response = requests.get(url)

        # Debugging: Print API response
        print("API Response Code:", response.status_code)

        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            return articles
        else:
            print("Failed to fetch news.")
            return []

    def build(self):
        """Creates the Kivy UI layout."""
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        title_label = Label(
            text="Top News Headlines",
            font_size=32,
            bold=True,
            size_hint_y=None,
            height=50
        )
        layout.add_widget(title_label)

        scroll_view = ScrollView()
        news_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        news_grid.bind(minimum_height=news_grid.setter('height'))

        articles = self.fetch_news()
        if articles == "no_internet":
            news_grid.add_widget(Label(text="No Internet Connection", font_size=20, bold=True))
        elif articles:
            for article in articles:
                news_title = article.get("title", "No Title Available")
                news_desc = article.get("description") or "No description available"
                news_url = article.get("url", "#")

                news_item = BoxLayout(orientation="vertical", padding=10, size_hint_y=None, height=150)
                title = Label(text=news_title, font_size=20, bold=True, size_hint_y=None, height=40)
                description = Label(text=news_desc, font_size=16, size_hint_y=None, height=50)
                read_more = Button(text="Read More", size_hint_y=None, height=40)
                read_more.bind(on_release=lambda btn, url=news_url: self.open_url(url))

                news_item.add_widget(title)
                news_item.add_widget(description)
                news_item.add_widget(read_more)

                news_grid.add_widget(news_item)
        else:
            news_grid.add_widget(Label(text="No news articles available.", font_size=20, bold=True))

        scroll_view.add_widget(news_grid)
        layout.add_widget(scroll_view)
        return layout

    def open_url(self, url):
        """Opens the news article link in a web browser."""
        import webbrowser
        webbrowser.open(url)


if __name__ == "__main__":
    print("Internet Status:", check_internet())  # Should print True or False
    NewsApp().run()
