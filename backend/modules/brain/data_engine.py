"""
A.R.I.S.E. AI - Real-time Data Engine

Fetches weather, news, and stock data with concise responses.
"""

import os
import sys
import requests
import yfinance as yf
from datetime import datetime
from dotenv import load_dotenv

sys.path.append('..')
from tts_engine import TTSEngine

# Load environment variables
load_dotenv()


class DataEngine:
    """Real-time data fetching for weather, news, and stocks."""
    
    def __init__(self):
        """Initialize data engine with API keys."""
        self.weather_api = os.getenv('WEATHER_API_KEY')
        self.news_api = os.getenv('GNEWS_API_KEY')  # Using GNews API
        self.stock_api = os.getenv('STOCK_API_KEY')
        
        # Default location (can be changed)
        self.default_city = "New York"
        
        print("Data engine initialized")
    
    def speak_response(self, text: str):
        """Speak response using TTS engine."""
        try:
            tts = TTSEngine()
            tts.speak(text)
        except Exception as e:
            print(f"TTS error: {e}")
    
    def _get_country_name(self, country_code: str) -> str:
        """Get friendly country name from code."""
        country_map = {
            'us': 'United States',
            'in': 'India', 
            'uk': 'United Kingdom',
            'ca': 'Canada',
            'au': 'Australia',
            'de': 'Germany',
            'fr': 'France',
            'jp': 'Japan',
            'cn': 'China',
            'br': 'Brazil'
        }
        return country_map.get(country_code.lower(), country_code.upper())
    
    def get_weather(self, city: str = None) -> str:
        """
        Get current weather for a city.
        
        Args:
            city: City name (uses default if None)
            
        Returns:
            Weather description string
            
        Time: O(1), Space: O(1)
        """
        if not city:
            city = self.default_city
            
        try:
            url = f"http://api.weatherapi.com/v1/current.json"
            params = {
                'key': self.weather_api,
                'q': city,
                'aqi': 'no'
            }
            
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            
            if 'error' in data:
                return f"Sorry, couldn't find weather for {city}"
            
            current = data['current']
            location = data['location']
            
            temp_c = current['temp_c']
            condition = current['condition']['text']
            feels_like = current['feelslike_c']
            
            weather_msg = f"It's {temp_c}°C in {location['name']}, {condition.lower()}. Feels like {feels_like}°C."
            
            return weather_msg
            
        except Exception as e:
            return f"Weather service unavailable: {str(e)}"
    
    def get_news(self, topic: str = "general", country: str = "us") -> str:
        """
        Get latest news headlines using GNews API with location support.
        
        Args:
            topic: News category or search term
            country: Country code (us, in, uk, etc.)
            
        Returns:
            News summary string
            
        Time: O(1), Space: O(1)
        """
        try:
            # GNews API endpoint
            url = "https://gnews.io/api/v4/top-headlines"
            params = {
                'token': self.news_api,
                'lang': 'en',
                'country': country.lower(),
                'max': 3
            }
            
            # Add category if it's a valid one
            if topic and topic != "general":
                params['category'] = topic if topic in ['general', 'world', 'nation', 'business', 'technology', 'entertainment', 'sports', 'science', 'health'] else 'general'
            
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            
            if 'articles' not in data:
                return f"News service unavailable for {country.upper()} right now"
            
            articles = data.get('articles', [])
            if not articles:
                return f"No {topic} news found for {country.upper()}"
            
            headlines = []
            for i, article in enumerate(articles[:3], 1):
                title = article['title']
                # Clean up title - remove source if present
                if ' - ' in title:
                    title = title.split(' - ')[0]
                headlines.append(f"{i}. {title}")
            
            country_name = self._get_country_name(country)
            news_msg = f"Top {topic} news from {country_name}: " + ". ".join(headlines)
            
            return news_msg
            
        except Exception as e:
            return f"News service error: {str(e)}"
    
    def get_stock(self, symbol: str = "AAPL") -> str:
        """
        Get stock price information using yfinance.
        
        Args:
            symbol: Stock symbol (e.g., AAPL, ^NSEI for Nifty)
            
        Returns:
            Stock price string
            
        Time: O(1), Space: O(1)
        """
        try:
            symbol = symbol.upper()
            
            # Handle special indices
            if symbol in ['NIFTY', 'NIFTY50']:
                symbol = '^NSEI'
            elif symbol in ['SENSEX']:
                symbol = '^BSESN'
            elif symbol in ['DOW', 'DJIA']:
                symbol = '^DJI'
            elif symbol in ['NASDAQ']:
                symbol = '^IXIC'
            elif symbol in ['SP500', 'S&P500']:
                symbol = '^GSPC'
            
            # Create yfinance ticker
            ticker = yf.Ticker(symbol)
            
            # Get current data
            info = ticker.info
            hist = ticker.history(period="2d")
            
            if hist.empty:
                return f"No data available for {symbol}"
            
            current_price = hist['Close'].iloc[-1]
            prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            
            change = current_price - prev_close
            change_percent = (change / prev_close) * 100
            
            direction = "up" if change > 0 else "down" if change < 0 else "unchanged"
            
            # Get friendly name
            name = info.get('longName', symbol)
            if name == symbol:
                # For indices, use common names
                index_names = {
                    '^NSEI': 'Nifty 50',
                    '^BSESN': 'Sensex',
                    '^DJI': 'Dow Jones',
                    '^IXIC': 'Nasdaq',
                    '^GSPC': 'S&P 500'
                }
                name = index_names.get(symbol, symbol)
            
            # Format price based on value
            if current_price > 1000:
                price_str = f"{current_price:,.0f}"
            else:
                price_str = f"{current_price:.2f}"
            
            stock_msg = f"{name} is {price_str}, {direction} {abs(change):.2f} or {abs(change_percent):.2f}% today"
            
            return stock_msg
            
        except Exception as e:
            return f"Stock data error for {symbol}: {str(e)}"
    
    def process_data_request(self, user_input: str) -> str:
        """
        Process user request for weather, news, or stock data.
        
        Args:
            user_input: User's request
            
        Returns:
            Appropriate data response
        """
        user_lower = user_input.lower()
        
        # Weather requests
        if any(word in user_lower for word in ['weather', 'temperature', 'temp', 'hot', 'cold', 'rain', 'sunny']):
            # Try to extract city name - improved extraction
            city = None
            words = user_input.split()
            
            # Look for "in [city]", "of [city]", "at [city]", "on [city]" patterns
            for i, word in enumerate(words):
                if word.lower() in ['in', 'of', 'at', 'on'] and i + 1 < len(words):
                    city = words[i + 1].title()
                    # Handle multi-word cities
                    if i + 2 < len(words) and words[i + 2].istitle():
                        city += " " + words[i + 2].title()
                    break
            
            # If no preposition found, look for proper nouns
            if not city:
                for word in words:
                    if word.istitle() and word.lower() not in ['weather', 'temperature', 'temp', 'today', 'what', 'is']:
                        city = word
                        break
            
            response = self.get_weather(city)
            self.speak_response(response)
            return response
        
        # Stock requests
        elif any(word in user_lower for word in ['stock', 'share', 'price', 'trading', 'market']):
            # Try to extract stock symbol - improved extraction
            symbol = None
            words = user_input.split()
            
            # Common company names to symbols mapping
            company_symbols = {
                'apple': 'AAPL', 'google': 'GOOGL', 'tesla': 'TSLA', 'microsoft': 'MSFT',
                'amazon': 'AMZN', 'meta': 'META', 'facebook': 'META', 'nvidia': 'NVDA',
                'netflix': 'NFLX', 'uber': 'UBER', 'disney': 'DIS', 'walmart': 'WMT',
                'coca cola': 'KO', 'pepsi': 'PEP', 'intel': 'INTC', 'amd': 'AMD',
                'ibm': 'IBM', 'oracle': 'ORCL', 'salesforce': 'CRM', 'adobe': 'ADBE',
                'zoom': 'ZM', 'twitter': 'TWTR', 'snapchat': 'SNAP', 'spotify': 'SPOT',
                # Indian stocks
                'reliance': 'RELIANCE.NS', 'tcs': 'TCS.NS', 'infosys': 'INFY.NS',
                'hdfc': 'HDFCBANK.NS', 'icici': 'ICICIBANK.NS', 'wipro': 'WIPRO.NS',
                # Indices
                'nifty': 'NIFTY', 'nifty50': 'NIFTY', 'sensex': 'SENSEX',
                'dow': 'DOW', 'nasdaq': 'NASDAQ', 'sp500': 'SP500', 's&p500': 'SP500'
            }
            
            # Look for company names
            user_text = user_input.lower()
            for company, sym in company_symbols.items():
                if company in user_text:
                    symbol = sym
                    break
            
            # Look for direct stock symbols (all caps words)
            if not symbol:
                for word in words:
                    if word.isupper() and len(word) >= 2 and len(word) <= 5:
                        symbol = word
                        break
            
            # Look for "of [company]" patterns
            if not symbol:
                for i, word in enumerate(words):
                    if word.lower() == 'of' and i + 1 < len(words):
                        next_word = words[i + 1].lower()
                        if next_word in company_symbols:
                            symbol = company_symbols[next_word]
                            break
                        # Try the word as a symbol
                        elif len(words[i + 1]) <= 5:
                            symbol = words[i + 1].upper()
                            break
            
            # Default fallback
            if not symbol:
                symbol = "AAPL"
            
            response = self.get_stock(symbol)
            self.speak_response(response)
            return response
        
        # News requests  
        elif any(word in user_lower for word in ['news', 'headlines', 'latest', 'happening']):
            # Try to extract location/country
            country = "us"  # Default
            topic = "general"
            
            # Country mapping
            countries = {
                'india': 'in', 'indian': 'in',
                'america': 'us', 'american': 'us', 'usa': 'us', 'united states': 'us',
                'britain': 'uk', 'british': 'uk', 'england': 'uk', 'uk': 'uk',
                'canada': 'ca', 'canadian': 'ca',
                'australia': 'au', 'australian': 'au',
                'germany': 'de', 'german': 'de',
                'france': 'fr', 'french': 'fr',
                'japan': 'jp', 'japanese': 'jp',
                'china': 'cn', 'chinese': 'cn'
            }
            
            # Extract country from user input
            for country_name, country_code in countries.items():
                if country_name in user_lower:
                    country = country_code
                    break
            
            # Extract topic
            topics = ['business', 'technology', 'sports', 'health', 'science']
            for top in topics:
                if top in user_lower:
                    topic = top
                    break
            
            response = self.get_news(topic, country)
            self.speak_response(response)
            return response
        
        else:
            return None  # Not a data request


def main():
    """Test the data engine."""
    engine = DataEngine()
    
    # Test weather
    print("Testing weather...")
    weather = engine.get_weather("London")
    print(f"Weather: {weather}")
    engine.speak_response(weather)
    
    # Test news
    print("\nTesting news...")
    news = engine.get_news("technology")
    print(f"News: {news}")
    engine.speak_response(news)
    
    # Test stock
    print("\nTesting stock...")
    stock = engine.get_stock("AAPL")
    print(f"Stock: {stock}")
    engine.speak_response(stock)


if __name__ == "__main__":
    main()
