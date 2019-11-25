import scrapy
import json
import re

from bs4 import BeautifulSoup

class RestaurantsSpider(scrapy.Spider):
    name = "restaurants"

    cities_filename = "cities.json"
    output_filename = "restaurants.json"

    hrefs_pattern = "/Restaurant_Review(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+"
    home_url = "https://www.tripadvisor.ru/"

    def start_requests(self):
        with open(self.cities_filename, "r") as cities_file:
            datastore = json.load(cities_file)
            for city in datastore:
                yield scrapy.Request(
                    url=city["url"], callback=self.parse_restaurants_urls
                )

    def parse_restaurants_urls(self, response):
        html = response.body.decode("utf-8")
        restaurants_urls = re.findall(self.hrefs_pattern, html)

        for url in restaurants_urls:
            restaurant_url = self.home_url + url
            yield scrapy.Request(url=restaurant_url, callback=self.parse)

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, "html.parser")

        yield {
            "url": response.url,
            "title": soup.find("h1", class_="ui_header").get_text(),
            "rating": soup.find("span", class_="ui_bubble_rating").get("alt"),
            "review_count": soup.find("span", class_="reviewCount").get_text(),
            "street_adress": soup.find("span", class_="street-address").get_text(),
            "locality": soup.find("span", class_="locality").get_text(),
            "country_name": soup.find("span", class_="country-name").get_text(),
            "phone_number": soup.find(
                "span", class_="detail is-hidden-mobile"
            ).get_text(),
        }
