import scrapy 

class amazon(scrapy.Spider):
    name = 'amz'
    start_urls = ['https://www.amazon.in/s?k=samsung']
    custom_settings = {
        'CONCURRENT_REQUESTS' : 1
    }
    

    def parse(self,response):
        yield {
                'name' :response.css('span[class="a-size-medium a-color-base a-text-normal"]::text').extract(),
                'price':response.css('span[class = "a-price-whole"]::text').extract()
            }
        next_page = response.css('li[class = "a-last"] a::attr(href)').get()
        if next_page is not None:
            x = response.urljoin(next_page)
            yield scrapy.Request(x, callback=self.parse)
