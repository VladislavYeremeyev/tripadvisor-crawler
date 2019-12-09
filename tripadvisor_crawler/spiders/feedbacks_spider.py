import scrapy
import json
import re

from bs4 import BeautifulSoup

class FeedbacksSpider(scrapy.Spider):
    name = "feedbacks"

    restaurants_filename = "restaurants.json"
    output_filename = "feed.json"
    home_url = "https://www.tripadvisor.ru/"

    def start_requests(self):
        with open(self.restaurants_filename, "r") as restaurants_file:
            datastore = json.load(restaurants_file)

            for restaurant in datastore:
                yield scrapy.Request(url=restaurant["url"], callback=self.parse)

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, "html.parser")

        reviews = soup.find_all("div", class_="reviewSelector")
        reviews_data = {}

        for review in reviews:
            user_info = review.find("div", class_="pointer_cursor") or ""
            user_location_info = user_info.find("div", class_="userLoc") or ""
            user_location = user_location_info.find("strong").get_text() if user_location_info else ""
            reviews_data.update({
                "url": response.url,
                "user_location": user_location,
                "username": user_info.get_text().replace(user_location, ""),
                "date": review.find("span", class_="ratingDate").get_text() or "",
                "review_title": review.find("span", class_="noQuotes").get_text(),
                "review_body": review.find("p", class_="partial_entry").get_text(),
                "date_of_visit": review.find("div", class_="prw_reviews_stay_date_hsx").get_text()
            })

            user_badging_block = review.find("div", class_="memberBadgingNoText")
            badgings = user_badging_block.findAll("span", class_="badgetext")
            if user_badging_block.find("span", class_="pencil-paper"):
                reviews_data.update({'reviews_by_user_amount': badgings[0].get_text()})

                if user_badging_block.find("span", class_="thumbs-up-fill"):
                    reviews_data.update({"review_likes_amount": badgings[1].get_text()})
            elif user_badging_block.find("span", class_="thumbs-up-fill"):
                reviews_data.update({"review_likes_amount": badgings[0].get_text()})
            else:
                reviews_data.update({"review_likes_amount": ''})

            for x in range(1, 6):
                if review.find("span", class_=f'bubble_{x}0'):
                    reviews_data.update({"stars_amount": x})

            yield reviews_data

        # next_page = home_url + response.css('.nav.next ::attr("href")').get()
        #
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)
