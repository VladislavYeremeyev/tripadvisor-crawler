# TripAdvisor Crawler

## Что сделано

- Crawler для списка городов России
- Crawler для получения данных о ресторанах

## Запуск

- [Установите](https://docs.scrapy.org/en/latest/intro/install.html) Scrapy и необходимое окружение.
- [Установите](https://pypi.org/project/beautifulsoup4/) Beautiful Soup - `pip3 install beautifulsoup4`.

- Находясь в корне репозитория, выполните команду, собирающую список городов России в `json`-файл:

```bash
scrapy runspider tripadvisor_crawler/spiders/cities_spider.py -t json -o - > cities.json
```

- Парсинг данных о ресторанах России в `json`-файл, используя список городов, полученных на прошлом шаге:

```bash
scrapy runspider tripadvisor_crawler/spiders/restaurants_spider.py -t json -o - > restaurants.json
```

- Парсинг данных об отзывах по каждому из ресторанов России в `json`-файл, используя список ресторанов, полученных на прошлом шаге:

```bash
scrapy runspider tripadvisor_crawler/spiders/reviews_spider.py -t json -o - > reviews.json
```

- Сбор статистики по ревью
```bash
python3 tripadvisor_crawler/statistics.py
```
