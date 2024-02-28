import scrapy
from scrapy.crawler import CrawlerProcess

from packages_from_homework_8.seed import load_json_data, data_seed


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "data/quotes.json"}
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield {
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").extract_first(),
                "quote": quote.xpath("span[@class='text']/text()").get().strip(),
            }
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(
                url=self.start_urls[0] + next_link, callback=self.parse
            )


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "data/authors.json"}
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]
    about_urls = set()

    def parse(self, response):
        # check if program already parsed about page
        if response.xpath("/html//div[@class='author-description']/text()").get():
            yield {
                "fullname": response.xpath("/html//h3/text()").get(),
                "born_date": response.xpath(
                    "/html//span[@class='author-born-date']/text()"
                ).get(),
                "born_location": response.xpath(
                    "/html//span[@class='author-born-location']/text()"
                ).get(),
                "description": response.xpath(
                    "/html//div[@class='author-description']/text()"
                ).get(),
            }

        # prepare set of about pages urls to parse
        for quote in response.xpath("/html//div[@class='quote']"):
            self.about_urls.add(quote.xpath("span/a/@href").get())
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(
                url=self.start_urls[0] + next_link, callback=self.parse
            )

        # if o more quotes pages to parse, parse about pages
        for about_url in self.about_urls:
            yield scrapy.Request(
                url=self.start_urls[0] + about_url, callback=self.parse
            )


def main():
    # run spider
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.crawl(AuthorsSpider)
    process.start()

    print("Seeding data in database using packages from homework #8...")
    authors = load_json_data("data/authors.json")
    quotes = load_json_data("data/quotes.json")
    data_seed(authors, quotes)
    print("All done!")


if __name__ == "__main__":
    main()
