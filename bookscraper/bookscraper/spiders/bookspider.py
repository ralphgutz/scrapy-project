import scrapy
from bookscraper.items import BookItem


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            relative_url = book.css('h3 a::attr(href)').get()  # Relative URL of book

            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url

            yield response.follow(book_url, callback=self.parse_book_page)  # Go to webpage of each book


        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:  # If element in next_page exists (next page button)
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page

            yield response.follow(next_page_url, callback=self.parse)  # Run self.parse() to crawl next page


    def parse_book_page(self, response):  # Parse each book detail (each book has its own webpage)
        table_row = response.css('table tr')

        book_item = BookItem()

        book_item['url'] = response.url
        book_item['title'] = response.css('.product_main h1::text').get()
        book_item['product_type'] = table_row[1].css('td::text').get()
        book_item['price_excl_tax'] = table_row[2].css('td::text').get()
        book_item['price_incl_tax'] = table_row[3].css('td::text').get()
        book_item['tax'] = table_row[4].css('td::text').get()
        book_item['availability'] = table_row[5].css('td::text').get()
        book_item['num_reviews'] = table_row[6].css('td::text').get()
        book_item['stars'] = response.css('p.star-rating::attr(class)').get()
        book_item['category'] = response.xpath('//*[@id="default"]/div/div/ul/li[3]/a').css('a::text').get()  # XPath of an element (check in scrapy shell, use Chrome to copy XPath)
        book_item['description'] = response.xpath('//*[@id="content_inner"]/article/p').css('p::text').get()
        book_item['price'] = response.css('.price_color::text').get()

        yield book_item
        