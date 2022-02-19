from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

CHROME_DRIVER_PATH = "C:\Development\chromedriver.exe"


# Web scraper(Bot)
class SteamData:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        self.driver.get("https://steamdb.info/")

        self.all_games = self.driver.find_elements(By.CLASS_NAME, "css-truncate")
        self.all_games_text = [game.text for game in self.all_games[1:]]

        self.all_statues = self.driver.find_elements(By.CLASS_NAME, "green")
        self.all_statues_text = [status.text for status in self.all_statues[1:]]

        self.all_peaks_and_prices = self.driver.find_elements(By.CLASS_NAME, "text-center")
        self.all_peaks_and_prices_text = [peak_and_price.text for peak_and_price in self.all_peaks_and_prices[2:] if peak_and_price not in self.all_statues]

        self.all_prices = [price for price in self.all_peaks_and_prices_text if price == "Free" or "$" in price]

    def most_played(self):
        """Gets the Most Played statistics and put them into a CSV file"""
        most_played_games = [game for game in self.all_games_text[:15]]
        players_now = [player for player in self.all_statues_text[:15]]
        peaks_today = [peak for peak in self.all_peaks_and_prices_text[:15]]

        most_played_statistics = {
            "Most Played": most_played_games,
            "Players Now": players_now,
            "Peak Today": peaks_today
        }
        most_played_df = pd.DataFrame(most_played_statistics)
        most_played_df.to_csv("Most-Played-Games.csv")

    def trending(self):
        """Gets the Trending statistics and put them into a CSV file"""
        trending_games = [game for game in self.all_games_text[15:30]]
        players_now = [player for player in self.all_statues_text[15:30]]

        trending_games_statistics = {
            "Trending": trending_games,
            "Players Now": players_now
        }
        trending_games_df = pd.DataFrame(trending_games_statistics)
        trending_games_df.to_csv("Trending-Games.csv")

    def releases(self):
        """Gets the Releases statistics and put them into a CSV file"""
        games_released = [game for game in self.all_games_text[30:45]]
        releases_peaks = [peak for peak in self.all_statues_text[30:45]]
        releases_prices = [price for price in self.all_prices[:15]]

        releases_statistics = {
            "Releases": games_released,
            "Peaks Today": releases_peaks,
            "Price": releases_prices
        }
        releases_df = pd.DataFrame(releases_statistics)
        releases_df.to_csv("Releases.csv")

    def hot_releases(self):
        """Gets the Hot Releases statistics and put them into a CSV file"""
        hot_releases_games = [game for game in self.all_games_text[45:]]
        hot_releases_ratings = [rating for rating in self.all_statues_text[45:]]
        hot_releases_prices =[price for price in self.all_prices[15:]]

        hot_releases_statistics = {
            "Hot Releases": hot_releases_games,
            "Rating": hot_releases_ratings,
            "Price": hot_releases_prices
        }
        hot_releases_df = pd.DataFrame(hot_releases_statistics)
        hot_releases_df.to_csv("Hot-Releases.csv")


if __name__ == "__main__":
    steam_data = SteamData()

    # Get all data and put them in different CSV files
    steam_data.most_played()
    steam_data.trending()
    steam_data.releases()
    steam_data.hot_releases()

    steam_data.driver.close()
