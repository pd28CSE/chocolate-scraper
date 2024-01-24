import scrapy
import re

from chocolatescraper.items import ChocolatescraperItem
from chocolatescraper.itemsloaders import ChocolateProductLoader


class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):
        products = response.css("product-item")
        pattern = re.compile(r"[a-zA-Z\-\.\'\"\<\>\=\/\ ^\n]")

        for product in products:
            chocolate_product_loader = ChocolateProductLoader(
                item=ChocolatescraperItem(),
                selector=product,
            )
            chocolate_product_loader.add_css("name", "a.product-item-meta__title::text")
            chocolate_product_loader.add_css(
                "price",
                "span.price",
                re='<span class="price">\n              <span class="visually-hidden">Sale price</span>(.*)</span>',
            )
            chocolate_product_loader.add_css(
                "url", "div.product-item-meta a::attr(href)"
            )

            # chocolate_scrape_irtem["name"] = product.css(
            #     "a.product-item-meta__title::text"
            # ).get()
            # chocolate_scrape_irtem["price"] = re.sub(
            #     pattern, "", product.css("span.price").get()
            # )
            # chocolate_scrape_irtem["url"] = product.css(
            #     "div.product-item-meta a"
            # ).attrib["href"]

            # yield chocolate_scrape_irtem

            yield chocolate_product_loader.load_item()

        next_page = response.css('[rel="next"] ::attr(href)').get()
        # next_pagee = response.css('[rel="next"]').attrib["href"]
        # print("==", next_pagee)
        if next_page is not None:
            next_page_url = "https://www.chocolate.co.uk" + next_page
            yield response.follow(next_page_url, callback=self.parse)
