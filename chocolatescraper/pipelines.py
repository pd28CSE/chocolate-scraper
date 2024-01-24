from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

import psycopg2


class SavingToPostgresPipeline(object):
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="chocolate_scraping",
            user="postgres",
            password="postgres",
        )
        self.cure = self.connection.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        # we need to return the item below as scrapy expects us to!
        return item

    def store_in_db(self, item):
        self.curr.execute(
            """ insert into chocolate_products values (%s,%s,%s)""",
            (item["name"][0], item["price"][0], item["url"][0]),
        )
        self.conn.commit()


class ChocolatescraperPipeline:
    gbpToUsdRate = 1.3

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get("price"):
            price = float(adapter.get("price"))
            adapter["price"] = price * self.gbpToUsdRate
            return item

        else:
            raise DropItem(f"Missing price in {item}")


class DuplicatesPipeline:
    def __init__(self):
        self.price_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter["name"] in self.price_seen:
            raise DropItem(f"Duplicate item found: {item!r}")

        else:
            self.price_seen.add(adapter["name"])
            return item
