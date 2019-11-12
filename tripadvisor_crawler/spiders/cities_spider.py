import scrapy

home_url = 'https://www.tripadvisor.ru'

class CitiesSpider(scrapy.Spider):
    name = 'cities'
    start_urls = [
        home_url + '/Restaurants-g294459-oa20-Russia.html',
    ]

    def parse(self, response):
        # for city in response.css('.geo_wrap'):
        #     yield {
        #         'name': city.css('.geo_name a::text').get(),
        #         'url': home_url + city.css('.geo_name a::attr(href)').get(),
        #     }

        # next_page = home_url + response.css('.pageNumbers a.pageNum.taLnk::attr("href")').get()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)

        for city in response.css('.geoList li'):
            yield {
                'name': city.css('a::text').get(),
                'url': home_url + city.css('a::attr(href)').get(),
            }

        next_page = home_url + response.css('.pgLinks a.guiArw.sprite-pageNext ::attr("href")').get()

        if next_page is not None:
            yield response.follow(next_page, self.parse)