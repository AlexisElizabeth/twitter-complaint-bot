from internet_speed_twitter_bot import *

PROMISED_DOWN = 150
PROMISED_UP = 10
CHROME_DRIVER_PATH = "C:\Development\chromedriver.exe"

if __name__ == "__main__":
    bot = InternetSpeedTwitterBot(CHROME_DRIVER_PATH, PROMISED_UP, PROMISED_DOWN)
    bot.get_internet_speed()

    if bot.promised_download_speed > bot.real_download_speed or bot.promised_upload_speed > bot.real_upload_speed:
        bot.tweet_at_provider()
