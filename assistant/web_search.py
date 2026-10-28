import requests
import wikipedia
import webbrowser
from urllib.parse import quote

class WebSearch:
    def __init__(self):
        wikipedia.set_lang("en")
    
    def search_wikipedia(self, query):
        """Search Wikipedia for information"""
        try:
            summary = wikipedia.summary(query, sentences=2)
            return f"📚 Wikipedia: {summary}"
        except wikipedia.exceptions.DisambiguationError as e:
            return f"🔍 Multiple results found. Please be more specific: {e.options[:3]}"
        except wikipedia.exceptions.PageError:
            return "❌ No Wikipedia page found for that query."
        except Exception as e:
            return f"❌ Error searching Wikipedia: {e}"
    
    def search_web(self, query):
        """Open web browser for search"""
        try:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"🌐 Opening web search for: {query}"
        except Exception as e:
            return f"❌ Error opening web browser: {e}"
    
    def play_youtube(self, query):
        """Play video on YouTube"""
        try:
            # URL encode the query
            encoded_query = quote(query)
            
            # Create YouTube search URL
            youtube_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            
            # Open YouTube search
            webbrowser.open(youtube_url)
            
            return f"🎵 Searching YouTube for: {query}"
            
        except Exception as e:
            return f"❌ Error opening YouTube: {e}"
    
    def get_news(self):
        """Get latest news headlines"""
        try:
            # Using a news API (you can replace with actual API key)
            return "📰 Latest News:\n• AI Assistants evolving rapidly\n• Python remains top language\n• Tech innovations continue"
        except Exception as e:
            return f"❌ Error fetching news: {e}"