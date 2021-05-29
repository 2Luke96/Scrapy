import scrapy
import urllib
from scrapy.http.request.form import FormRequest


class AsambleaMadrid(scrapy.Spider):
    name = "Asamblea_Madrid"


    def parse(self, response):
            ids_re = r'WebForm_PostBackOptions\(([^,]*)'
            for id in response.css('#moduloBusqueda li a').re(ids_re):
                target = urllib.unquote(id).strip('"')
                formdata = {'__EVENTTARGET': target}
                request = FormRequest.from_response(response=response,
                                                    formdata=formdata,
                                                    callback=self.takeEachParty,
                                                    dont_click=True)
                yield request