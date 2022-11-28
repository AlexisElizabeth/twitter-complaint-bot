from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os

TWITTER_EMAIL = os.getenv("TWITTER_EMAIL")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")


class InternetSpeedTwitterBot:
    def __init__(self, chrome_driver_path, promised_up, promised_down):
        driver_service = Service(executable_path=chrome_driver_path)
        self.driver = webdriver.Chrome(service=driver_service)
        self.up = promised_up
        self.down = promised_down
        self.real_download_speed = 0
        self.real_upload_speed = 0
        self.promised_upload_speed = promised_up
        self.promised_download_speed = promised_down

    def get_internet_speed(self):
        url = "https://www.speedtest.net/"
        self.driver.get(url)
        accept_cookies_button = self.driver.find_element(By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]')
        accept_cookies_button.click()
        time.sleep(2)
        speed_test_go = self.driver.find_element(By.XPATH,
                                                 value='//*[@id="container"]/div/div[3]/'
                                                       'div/div/div/div[2]/div[3]/div[1]/a/span[4]')
        speed_test_go.click()
        time.sleep(60)

        # back_to_test_results_button = self.driver.find_element(By.XPATH, value='//*[@id="container"]/div/
        # div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[8]/div/div/div[2]/a')
        # back_to_test_results_button.click()

        real_download_speed = self.driver.find_element(By.XPATH, value='//*[@id="container"]/div/div[3]/div/'
                                                                       'div/div/div[2]/div[3]/div[3]/div/div[3]/div/'
                                                                       'div/div[2]/div[1]/div[1]/div/div[2]/span')
        self.real_download_speed = float(real_download_speed.text)
        real_upload_speed = self.driver.find_element(By.XPATH, value='//*[@id="container"]/div/div[3]/div/div/div/'
                                                                     'div[2]/div[3]/div[3]/div/div[3]/div/div/'
                                                                     'div[2]/div[1]/div[2]/div/div[2]/span')
        self.real_upload_speed = float(real_upload_speed.text)

    def tweet_at_provider(self):
        url = "https://twitter.com/login"
        self.driver.get(url)
        time.sleep(2)
        user_name_box = self.driver.find_element(By.NAME, value='text')

        user_name_box.click()
        user_name_box.send_keys(TWITTER_EMAIL)
        time.sleep(2)
        user_name_box.send_keys(Keys.ENTER)
        time.sleep(2)
        password = self.driver.find_element(By.NAME, value='password')
        password.send_keys(TWITTER_PASSWORD)
        password.send_keys(Keys.ENTER)
        time.sleep(5)
        tweet = self.driver.find_element(By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/header/'
                                                         'div/div/div/div[1]/div[3]/a/div')
        tweet.click()
        time.sleep(2)
        active = self.driver.switch_to.active_element
        active.send_keys(f"Hey Telenor, why is my internet speed "
                         f"{self.real_download_speed}down/{self.real_upload_speed}up "
                         f"when it's supposed to be {self.promised_download_speed}down/{self.promised_upload_speed}?")
        time.sleep(1)
        tweet_send = self.driver.find_element(By.XPATH, value='//*[@id="layers"]/div[2]/div/div/div/div/div/'
                                                              'div[2]/div[2]/div/div/div/div[3]/div/div[1]/'
                                                              'div/div/div/div/div[2]/div[3]/div/div/div[2]/div[4]')
        tweet_send.click()
