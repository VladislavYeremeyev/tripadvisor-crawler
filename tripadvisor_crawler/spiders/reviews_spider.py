import scrapy
import json
import re

from bs4 import BeautifulSoup


class ReviewsSpider(scrapy.Spider):
    name = "reviews"

    restaurants_filename = "restaurants.json"
    output_filename = "reviews.json"
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
            user_location = (
                user_location_info.find("strong").get_text()
                if user_location_info
                else ""
            )

            restaurant_name = soup.find("h1", class_="ui_header")
            url = review.select(".quote a")[0]
            date = review.find("span", class_="ratingDate")
            review_title = review.find("span", class_="noQuotes")
            review_body = review.find("p", class_="partial_entry")
            date_of_visit = review.find("div", class_="prw_reviews_stay_date_hsx")

            reviews_data.update(
                {
                    "restaurant_name": restaurant_name.get_text()
                    if restaurant_name
                    else "",
                    "url": self.home_url + url["href"] or "",
                    "user_location": user_location,
                    "username": user_info.get_text().replace(user_location, "")
                    if user_info and user_info.get_text()
                    else "",
                    "date": date.get_text() if date else "",
                    "review_title": review_title.get_text() if review_title else "",
                    "review_body": "",
                    "date_of_visit": date_of_visit.get_text() if date_of_visit else "",
                }
            )

            user_badging_block = review.find("div", class_="memberBadgingNoText")
            badgings = user_badging_block.findAll("span", class_="badgetext")
            if user_badging_block.find("span", class_="pencil-paper"):
                reviews_data.update({"reviews_by_user_amount": badgings[0].get_text()})

                if user_badging_block.find("span", class_="thumbs-up-fill"):
                    reviews_data.update({"review_likes_amount": badgings[1].get_text()})
            elif user_badging_block.find("span", class_="thumbs-up-fill"):
                reviews_data.update({"review_likes_amount": badgings[0].get_text()})
            else:
                reviews_data.update({"review_likes_amount": ""})

            for x in range(1, 6):
                if review.find("span", class_=f"bubble_{x}0"):
                    reviews_data.update({"stars_amount": x})

            if review_body and "...Еще" in review_body.get_text():
                yield scrapy.Request(
                    url=self.home_url + url["href"],
                    callback=self.parse_full,
                    meta=reviews_data,
                )
            else:
                reviews_data.update(
                    {"review_body": review_body.get_text() if review_body else ""}
                )
                yield reviews_data

        next_page_href = response.css('.nav.next ::attr("href")').get() or None

        if next_page_href is not None:
            next_page = self.home_url + next_page_href
            yield response.follow(next_page, self.parse)

    def parse_full(self, response):
        html = response.body
        soup = BeautifulSoup(html, "html.parser")
        key_list = [
            "restaurant_name",
            "url",
            "user_location",
            "username",
            "date",
            "review_title",
            "review_body",
            "date_of_visit",
            "reviews_by_user_amount",
            "review_likes_amount",
            "stars_amount",
        ]
        meta = {key: response.meta.copy()[key] for key in key_list}
        meta.update({"review_body": soup.find("p", class_="partial_entry").get_text()})
        yield meta
