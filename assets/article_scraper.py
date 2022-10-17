import os
import re
import urllib.request

from bs4 import BeautifulSoup
from selenium import webdriver


class Article:
    _html = None
    _article_text = None
    _article_title = None
    _text_list = None
    _article_image = None

    def __init__(self, url: str):

        driver = webdriver.Safari()
        driver.get(url)

        self._html = BeautifulSoup(driver.page_source, "lxml")
        self._article_text = None
        self._article_title = None
        self._text_list = []
        self._article_image = None

    def scrape_title(self):
        """
        Scrapes given url for article title.
        """
        find_heading = self._html.find(class_="article__heading")
        for heading in find_heading:
            heading = str(heading)
            self._article_title = re.sub(re.compile("<.*?>"), "", heading)
            self._article_title = self._article_title.capitalize()

    def scrape_text(self):
        """
        Scrapes given url for article title.
        """
        subscription_text = "$1.99per week Share this article Reminder, this is a Premium article and requires a subscription to read."
        find_article = self._html.find_all(class_="article__body")
        content = find_article[0].find_all("p")
        for line in content:
            line = str(line)
            text = re.sub(re.compile("<.*?>"), "", line)
            text = text.replace("\n", " ")
            self._text_list.append(text)
        self._article_text = " ".join(self._text_list)
        self._article_text = self._article_text.replace(subscription_text, "").strip()

    def scrape_image(self):
        """
        Scrapes given url for article header image.
        """
        all_img_tags = self._html.find_all("img")
        img_tags = str(all_img_tags)
        images = img_tags.split(",")
        for image in images:
            if "1440x810" not in image:
                continue

            pattern = re.compile(r"^.*?\.jpg")
            image_url = pattern.findall(image)

            self._article_image = self.download_image(image_url[0])

            break

    def download_image(self, url) -> str:
        if isinstance(url, str):
            self._article_title = re.sub(r"[^a-zA-Z0-9]", "", self._article_title)

            try:
                os.mkdir("./assets/images/")
            except:
                pass

            image_file_path = f"./assets/images/{self._article_title}.jpg"
            urllib.request.urlretrieve(url, image_file_path)

            return image_file_path

    @property
    def article_title(self):
        if not self._article_title:
            self.scrape_title()

        return self._article_title

    @property
    def article_text(self):
        if not self._article_text:
            self.scrape_text()

        return self._article_text

    @property
    def article_image(self):
        if not self._article_image:
            self.scrape_image()

        return self._article_image
