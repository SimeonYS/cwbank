import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import CcwbankItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class CcwbankSpider(scrapy.Spider):
	name = 'cwbank'
	start_urls = ['https://www.cwbank.com/en/blog-topics']

	def parse(self, response):
		post_links = response.xpath('//a[@class="list-item"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//div[@class="hero-overlay-content"]/div/span/text()').get()
		title = response.xpath('//div[@class="hero-overlay-content"]/div/h1/text()').get().strip()
		content = response.xpath('//div[@class="hero-overlay-content"]/div/p//text()').getall() + response.xpath('//div[@class="text-editor-content"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=CcwbankItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
