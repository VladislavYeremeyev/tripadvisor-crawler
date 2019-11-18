import scrapy
import json
import re

class RestaurantsSpider(scrapy.Spider):
    name = "restaurants"

    cities_filename = "cities.json"
    output_filename = "restaurants.json"

    hrefs_pattern = "/Restaurant_Review(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
    home_url = "https://www.tripadvisor.ru/"

    def start_requests(self):
        with open(self.cities_filename, "r") as cities_file:
            datastore = json.load(cities_file)
            for city in datastore:
                yield scrapy.Request(url=city["url"], callback=self.parse_restaurants_urls)

    def parse_restaurants_urls(self, response):
        html = response.body.decode('utf-8')
        restaurants_urls = re.findall(self.hrefs_pattern, html)

        print(restaurants_urls)
        print(len(restaurants_urls))

        for url in restaurants_urls:
            restaurant_url = self.home_url + url
            print(restaurant_url)
            yield scrapy.Request(url=restaurant_url, callback=self.parse)


    def parse(self, response):
        html = response.body.decode('utf-8')

        {
            title: response.css("h1.ui_header::text").get()
        }
