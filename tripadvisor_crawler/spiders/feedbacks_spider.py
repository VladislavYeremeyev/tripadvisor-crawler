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

            for restaurant in datastore:
                yield scrapy.Request(url=restaurant["url"], callback=self.parse)

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, "html.parser")
        home_url = "https://www.tripadvisor.ru/"

        assessments = soup.find("div", class_="choices").find_all(
            "div", class_="ui_checkbox item"
        )
        assessments_data = {}

        for assessment in assessments:
            metric_name = assessment.find("input").get("value") + "_star"
            review_amount = assessment.find("span", class_="row_num").get_text()

            assessments_data[metric_name] = review_amount

        reviews = soup.find_all("div", class_="reviewSelector")
        reviews_data = {}

        for review in reviews:
            user_info = review.find("div", class_="pointer_cursor") or ""
            user_location_info =  user_info.find("div", class_="userLoc") or ""

            reviews_data["user_location"] = user_location_info.find("strong").get_text() if user_location_info else ""
            reviews_data["username"] = user_info.get_text().replace(reviews_data["user_location"], "")
            reviews_data["date"] = review.find("span", class_="ratingDate").get_text() or ""

            user_badging_block = review.find("div", class_="memberBadgingNoText")
            badgings = user_badging_block.findAll("span", class_="badgetext")
            reviews_data["review_likes_amount"] = ""

            if user_badging_block.find("span", class_="pencil-paper"):
                reviews_data["reviews_by_user_amount"] = badgings[0].get_text()

                if user_badging_block.find("span", class_="thumbs-up-fill"):
                    reviews_data["review_likes_amount"] = badgings[1].get_text()

            elif user_badging_block.find("span", class_="thumbs-up-fill"):
                reviews_data["review_likes_amount"] = badgings[0].get_text()

            reviews_data["review_title"] = review.find("span", class_="noQuotes").get_text()
            reviews_data["review_body"] = review.find("p", class_="partial_entry").get_text()
            reviews_data["date_of_visit"] = review.find("div", class_="prw_reviews_stay_date_hsx").get_text()

            yield {
                "username": reviews_data["username"],
                "location": reviews_data["user_location"],
                "review_likes_amount": reviews_data["review_likes_amount"],
                "date": reviews_data["date"],
                "review_title": reviews_data["review_title"],
                "review_body": reviews_data["review_body"],
                "date_of_visit": reviews_data["date_of_visit"],
                "review_count": soup.find("span", class_="reviews_header_count").get_text(),
                "assessments_info": assessments_data,
                "reviews": reviews_data
            }

            next_page = home_url + response.css('.nav.next ::attr("href")').get()

            if next_page is not None:
                yield response.follow(next_page, self.parse)
