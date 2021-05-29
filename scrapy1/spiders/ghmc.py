import scrapy
from bs4 import BeautifulSoup as bs


class ghmcspider(scrapy.Spider):
    name = "ghmc"
    start_urls = [
        'https://www.ghmc.gov.in/covid_details.aspx'
    ]

    def parse(self, response):
        __VIEWSTATE = response.xpath('//*[@name="__VIEWSTATE"]/@value').get()
        # __EVENTTARGET = 'ctl00$ContentPlaceHolder1$grdReport'
        # EVENTARGUMENT = iter(['page$'+str(i) for i in range(1,10)]),
        __VIEWSTATEGENERATOR = response.xpath('//*[@name="__VIEWSTATEGENERATOR"]/@value').get()
        __EVENTVALIDATION = response.xpath('//*[@name="__EVENTVALIDATION"]/@value').get()
        
        print("__VIEWSTATEGENERATOR is ", __VIEWSTATEGENERATOR)


        form = {
            'VIEWSTATE' :__VIEWSTATE ,
            'EVENTTARGET' :'ctl00$ContentPlaceHolder1$grdReport',
            'EVENTARGUMENT' : 'Page$4',
            "VIEWSTATEGENERATOR" : __VIEWSTATEGENERATOR,
            "EVENTVALIDATION" : __EVENTVALIDATION
        }
        yield scrapy.FormRequest(
           response.url , formdata = form, callback=self.parse_data)

    def parse_data(self,response):
        for i in range(301):
            print(i)
            for content in response.xpath('//*[@id="ContentPlaceHolder1_grdReport"]'):
                yield {
                    'text': content.xpath('//*[@id="ContentPlaceHolder1_grdReport"]/tbody/tr[' + str(i) +']/td/font/span/text()').getall()
                    }


    def scrape_state_firms(self, state_item):
        '''
        Scrape all of the firm listed for a given state 
        '''
        self.br.open(self.url)

        s = bs(self.br.response().read())
        saved_form = s.find('form', id='form1').prettify()

        self.br.select_form('form1')
        self.br.form['ctl00$ContentPlaceHolder1$grdReport'] = [ state_item.name ]

# print '\n'.join(['%s:%s (%s)' % (c.name,c.value,c.disabled) for c in self.br.form.controls])

# k = iter(['page$'+str(i) for i in range(1,10)])
# for i in range(11):
    #  print(next(k))

# x = iter(["apple", "banana", "cherry"])
# for i in range(3):
#     print(next(x))
