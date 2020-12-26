# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class CoinSpider(scrapy.Spider):
    name = 'coin'
    allowed_domains = ['www.livecoin.net']

    script = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(1))
            usd_tab = assert(splash:select_all(".filterPanelItem___2z5Gb"))
            usd_tab[3]:mouse_click()
            assert(splash:wait(1))
            splash:set_viewport_full()
            return splash:png()
        end
    '''

    def start_requests(self):
        yield SplashRequest(url="https://www.livecoin.net", callback=self.parse, endpoint="execute", args={
            'lua_source': self.script
        })

    def parse(self, response):
        for currency in response.xpath("//div[contains(@class, 'ReactVirtualized__Table__row tableRow__3Etis ')]"):
            yield{
                'currency pair': currency.xpath(".//div[1]/div/text()").get(),
                'volume(24h)': currenty.xpath(".//div[2]/span/text()").get()
            }
