import scrapy


class QuotesSpider(scrapy.Spider):
    name = "yiwuProduct"

    def start_requests(self):
        url = 'https://tieba.baidu.com/f?ie=utf-8&kw=%E4%B9%89%E4%B9%8C%E5%BF%AB%E9%80%92&fr=search'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.threadlist_title.pull_left.j_th_tit '):
            yield {
                'titile': quote.css('a.j_th_tit::text').get(),
            }

        next_page = response.css('div.pagination-default.clearfix a.next.pagination-item::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


