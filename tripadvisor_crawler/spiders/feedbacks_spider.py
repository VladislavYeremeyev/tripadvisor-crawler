import scrapy
import json
import re

from bs4 import BeautifulSoup

class FeedbacksSpider(scrapy.Spider):
    name = "feedbacks"

    restaurants_filename = "restaurants.json"
    output_filename = "feed.json"

    def start_requests(self):
        with open(self.restaurants_filename, "r") as restaurants_file:
            datastore = json.load(restaurants_file)
            print("ok")
            for restaurant in datastore:
                print(restaurant["url"])
                yield scrapy.Request(
                    url=restaurant["url"], callback=self.parse
                )

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, "html.parser")

        assessments = soup.find("div", class_="choices").find_all("div", class_="ui_checkbox item")
        assessments_data = {}

        for assessment in assessments:
            metric_name = assessment.find("input").get("value") + "_star"
            review_amount = assessment.find("span", class_="row_num").get_text()

            assessments_data[metric_name] = review_amount

        reviews = soup.find("div", class_="reviewSelector")
        reviews_data = {}

        for review in reviews:
            user_info = review.find("div", class_="pointer_cursor")

            reviews_data["user_location"] = user_info.find("div", class_="userLoc").find("strong").get_text()
            reviews_data["username"] = user_info.get_text().replace(reviews_data["user_location"], "")

            user_badging_block = review.find("div", class_="memberBadgingNoText")
            badgings = user_badging_block.findAll("span", class_="badgetext")

            if user_badging_block.find("span", class_="pencil-paper"):
                reviews_data["reviews_by_user_amount"] = badgings[0].get_text()

                if user_badging_block.find("span", class_="thumbs-up-fill"):
                    reviews_data["review_likes_amount"] = badgings[1].get_text()

            elif user_badging_block.find("span", class_="thumbs-up-fill"):
                    reviews_data["review_likes_amount"] = badgings[0].get_text()

            reviews_data["date"] = review.find("span", class_="ratingDate").get_text()
            reviews_data["review_title"] = review.find("span", class_="noQuotes").get_text()
            reviews_data["review_body"] = review.find("p", class_="partial_entry").get_text()
            reviews_data["date_of_visit"] = review.find("span", class_="stay_date_label").get_text()

        yield {
            "review_count": soup.find("span", class_="reviews_header_count").get_text(),
            "assessments_info": assessments_data,
            "reviews": reviews_data
        }
