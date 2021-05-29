from urllib.parse import urljoin
import scrapy
from scrapy.selector.unified import _response_from_text 
import re
# import pandas as pd

class imbd(scrapy.Spider):
    name = 'imbd'
    start_urls = ['https://www.imdb.com/chart/top']
    global data
    data = {}

    def parse(self, response):
        for content in response.css("tr"):
            link = response.urljoin(content.css('td.titleColumn > a::attr(href)').get())
            yield scrapy.Request(link, callback=self.parse_links)
            # yield scrapy.Request(link,callback=self.top_cast)
    
    # def parse_cast(self, response):
    #     for content in response.css("tr"):
    #         link = response.urljoin(content.css('td.titleColumn > a::attr(href)').get())
    #         yield scrapy.Request(link,callback=self.top_cast)

    # def top_cast(self,response):
    #     for cast in response.css("a.StyledComponents__ActorName-y9ygcu-1.eyqFnv::attr(href)").getall():
    #         cast = re.sub('\?ref[\w\W]*',str('/bio'),cast)
    #         cast = response.urljoin(cast)
    #         yield scrapy.Request(cast, callback= self.cast_scrape)

    def parse_links(self,response):                                                                                                 
        data["title"] = response.css('h1 ::text').get()
        data["rating"] = response.css('span.AggregateRatingButton__RatingScore-sc-1il8omz-1.fhMjqK::text').get()
        data['summary'] = response.css("div.GenresAndPlot__TextContainerBreakpointS-cum89p-1.cUzKqw::text").get()
        for cast in response.css("a.StyledComponents__ActorName-y9ygcu-1.eyqFnv::attr(href)").getall():
            cast = re.sub('\?ref[\w\W]*',str('/bio'),cast)
            cast = response.urljoin(cast)
            yield scrapy.Request(cast, callback= self.cast_scrape)
        
            # 'storyline' : response.xpath('//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[7]/div[2]/div[1]/div[1]/div/text()').get()

        # pd.DataFrame(data, columns = ['title','rating','summary']).to_csv('Final_data.csv', encoding = 'utf-8', index= False)

    def cast_scrape(self,response):
        data['cast'] =  response.xpath('//*[@id="main"]/div[1]/div[1]/div/h3/a/text()').get()
        yield data  

