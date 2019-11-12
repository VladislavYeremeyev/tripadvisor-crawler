# TripAdvisor Crawler

## Что сделано

- Crawler для списка городов России

## Запуск

- [Установите](https://docs.scrapy.org/en/latest/intro/install.html) Scrapy и необходимое окружение.
- Находясь в корне репозитория, выполните команду, собирающую список городов России в `json`-файл:

```bash
scrapy runspider tripadvisor_crawler/spiders/cities_spider.py -t json -o - > cities.json
```
