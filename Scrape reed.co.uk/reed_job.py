import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ReedJobSpider(CrawlSpider):
    name = "reed_job"
    allowed_domains = ["www.reed.co.uk"]
    start_urls = ["https://www.reed.co.uk/jobs/it-jobs"]


    rules = (Rule(LinkExtractor(restrict_css='div.layout_content__49Kn9 > div > div > main div article div h2 a'), callback="parse_item", follow=False),
             Rule(LinkExtractor(restrict_css="ul.pagination a[aria-label='Next page']",deny='2'),follow=True)
             )

    def parse_item(self, response):
        title = response.css("div.job-header.row > div > div > h1::text").get()
        if title==None:
            title = response.css("div.col-xs-12 > h1::text").get()
        post_time = response.css("div.posted > span::text").get()
        if post_time==None:
            post_time='Nan'
        posted_by = response.css('div.posted > span > a > span::text').get()
        if posted_by==None or posted_by==[]:
            posted_by = 'Nan'
        salary_status = response.css('div.job-info--permament-icons > div:nth-child(1) > span > span:nth-child(2)::text').get()
        if salary_status == None:
            salary_status = response.css("div.mobile-metadata-container div.salary span[data-qa='salaryMobileLbl']::text").get()
        address =  response.css("div.job-info--permament-icons > div:nth-child(2) > span:nth-child(3) span::text").getall()
        if address==None or address==[]:
            address = response.css("div.mobile-metadata-container div.location  span:nth-child(3) span::text").getall()
            if address==None or address==[]:
                address = 'Nan'
        job_stat = response.css("span[data-qa='jobTypeLbl'] a::text").getall()
        if job_stat==None:
            job_stat = response.css("span[data-qa='jobTypeLbl'] a::text").getall()
            if job_stat==None or job_stat==[]:
                job_stat = 'Nan'
        req_skill = response.css('ul.list-unstyled.skills-list li::text').getall()
        if req_skill==None or req_skill==[]:
            req_skill = 'Nan'
        remote = response.css('div.mobile-metadata-container div.remote::text').getall()
        if remote==None or remote==[]:
            remote = 'Nan'

        yield {
            'title': title,
            'post_time': post_time,
            'posted_by': posted_by,
            'salary_status': salary_status,
            'address': address,
            'job_status': job_stat,
            'req_skill': req_skill,
            'Remote': remote,
            'Link':response.url,

        }
