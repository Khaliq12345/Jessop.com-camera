#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import scrapy

class camera(scrapy.Spider):
    name = 'cameras'
    allowed_domains = ['www.jessops.com']
    start_urls = ['https://www.jessops.com/cameras']
    custom_settings = {
       'FEED_URI' : 'tmp/drone.json'
   }
    
    def parse(self,response):
        for i in range(21,231, 21):
            products = response.xpath("//div[@class='image f-flex f-flex-column f-flex-space-between']")
            for product in products:
                urls = product.css('picture a').attrib['href']
                url = response.urljoin(urls)
                yield scrapy.Request(url = url, callback= self.parse_details)
         #pagination   
            next_page = f'https://www.jessops.com/cameras?fh_start_index={i}&fh_view_size=21'
            yield scrapy.Request(url = next_page,callback=self.parse)
            
    def parse_details(self,response):
        name = response.css('h1 span::text').extract_first()
        price = response.css('p.price::text').extract_first()
        delivery = response.css('li.home-delivery::text').extract_first()
        code = response.css('span.product-code-code::text').extract_first()
        tab = response.xpath("//div[@class='f-panel-box tab-contents f-accordion-content']")
        desc = tab.css('p::text').extract_first().strip()
        yield {
            'Name':name,
            'Price':price,
            'Delivery type': delivery,
            'Product code':code,
            'Description':desc
        }

