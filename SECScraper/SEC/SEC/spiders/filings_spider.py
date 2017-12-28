import scrapy
import re

class QuotesSpider(scrapy.Spider):
    name = "filings"

    def start_requests(self):
        urls = [
            'https://www.sec.gov/Archives/edgar/full-index/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.drilldown_to_idx)

    def drilldown_to_idx(self, response):
        hxs = scrapy.Selector(response)

        all_links = hxs.xpath('*//a/@href').extract()

        for link in all_links:
            #The top level will be the year, so let's check for that.
            pattern = re.compile("[0-9]+/")
            match = pattern.match(link)

            if match is None:
                #Next level is QTR1 to 4
                pattern = re.compile("QTR[1-4]/")
                match = pattern.match(link)

            if match is not None:
                yield scrapy.Request(url=response.url + link, callback=self.drilldown_to_idx)
            else:
                #Should have forms.idx which will have all the filings listed in it
                if "form.idx" in link:
                    print("Found form.idx")
                    yield scrapy.Request(url=response.url + link, callback=self.get_filings)

    def get_filings(self, response):
        filing_text = requests.get(response.url)
        
        lines = filing_text.splitlines()
        print(lines[10])


        #print(all_links)
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)