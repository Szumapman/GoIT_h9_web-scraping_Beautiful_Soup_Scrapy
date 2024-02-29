import json

import scrapy
from scrapy.crawler import CrawlerProcess

from packages_from_homework_8.seed import load_json_data, data_seed


QUOTES_AUTHORS = {"quotes": [], "authors": []}


class QuotesAuthorsSpider(scrapy.Spider):
    name = "quotes_authors"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]
    about_urls = set()
    def parse(self, response):
        if response.xpath("/html//div[@class='quote']"):
            for quote in response.xpath("/html//div[@class='quote']"):
                self.about_urls.add(quote.xpath("span/a/@href").get())
                yield QUOTES_AUTHORS["quotes"].append({
                    "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                    "author": quote.xpath("span/small/text()").extract_first(),
                    "quote": quote.xpath("span[@class='text']/text()").get().strip(),
                })
            next_link = response.xpath("//li[@class='next']/a/@href").get()
            if next_link:
                yield scrapy.Request(
                    url=self.start_urls[0] + next_link, callback=self.parse
                )
        elif response.xpath("/html//div[@class='author-description']/text()"):
            yield QUOTES_AUTHORS["authors"].append({
                "fullname": response.xpath("/html//h3/text()").get(),
                "born_date": response.xpath(
                    "/html//span[@class='author-born-date']/text()"
                ).get(),
                "born_location": response.xpath(
                    "/html//span[@class='author-born-location']/text()"
                ).get(),
                "description": response.xpath(
                    "/html//div[@class='author-description']/text()"
                ).get().strip(),
            })
        for about_url in self.about_urls:
            yield scrapy.Request(
                url=self.start_urls[0] + about_url, callback=self.parse
            )


def save_json_file(data: list, file_name: str) -> None:
    print(f"Saving {file_name} file...")
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(
            json.dumps(data, ensure_ascii=False, indent=4)
        )


def main():
    # run spider
    process = CrawlerProcess()
    process.crawl(QuotesAuthorsSpider)
    process.start()

    # save data
    save_json_file(QUOTES_AUTHORS["quotes"], "data/quotes.json")
    save_json_file(QUOTES_AUTHORS["authors"], "data/authors.json")

    print("Seeding data in database using packages from homework #8...")
    authors = load_json_data("data/authors.json")
    quotes = load_json_data("data/quotes.json")
    data_seed(authors, quotes)
    print("All done!")


if __name__ == "__main__":
    main()
