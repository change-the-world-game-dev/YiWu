import scrapy


class QuotesSpider(scrapy.Spider):
    name = "yiwuProduct"

    def start_requests(self):
        url = 'https://tieba.baidu.com/f?ie=utf-8&kw=%E4%B9%89%E4%B9%8C%E5%BF%AB%E9%80%92&fr=search'
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        response_page_link = response.css('div.threadlist_title.pull_left.j_th_tit a.j_th_tit')
        yield from response.follow_all(response_page_link, self.parse_response)

        for quote in response.css('div.threadlist_title.pull_left.j_th_tit '):
            yield {
                'titile': quote.css('a.j_th_tit::text').get(),
            }

        next_page = response.css('div.pagination-default.clearfix a.next.pagination-item::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


    def parse_response(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        for user_response in response.css('div.p_content'):
            yield {
                'content': extract_with_css('.d_post_content.j_d_post_content::text'),
                'username': extract_with_css('.d_name a.p_author_name.j_user_card::text'),
                'postTime': extract_with_css('.post-tail-wrap span.tail-info::text'),
            }