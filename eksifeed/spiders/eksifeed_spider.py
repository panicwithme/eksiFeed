# author = 'F. Cigdem Tosun'

import scrapy  
import urllib
import requests
from scrapy.http import Request
from urllib.parse import urljoin
from eksifeed.items import EksifeedItem

# verilen permalinkin halihazırda log.txt'de bulunup bulunmadığına bakar.
# bulunmuyorsa ekler ve false döner.
# sadece yeni entryleri görmek istediğim için böyle bir dosya var.
# tabi ki dosya yerine database de olur ancak şu anlık dosyayı tercih ediyorum.
def check_existence(plink):
    with open('log.txt', 'a+') as f:
        f.seek(0)
        permalinks = f.read().splitlines()
        if plink not in permalinks:
            f.write(plink)
            f.write("\n")
            return False
        return True

# verilen mesajı telegram botu üzerinden gönderir.
# url'deki API_KEY ve CHAT_ID yerlerini değiştirmeyi unutmayın.
def send_to_telegram(message):
    requests.get("https://api.telegram.org/bot[API_KEY]/sendMessage?chat_id=[CHAT_ID]&text={}".format(message))

class EksifeedSpider(scrapy.Spider): 
   name = "eksifeed" 
   allowed_domains = ["eksisozluk.com"] 
   
   # takip etmek istediğiniz başlıkların son sayfasının urlsini URL yerine koymayı unutmayın.
   # tabi mesaj olarak okumak isterseniz istediğiniz sayfadan başlayabilirsiniz.
   start_urls = [ 
      "[URL]",
   ]  

   def parse(self, response): 

      for full_entry in response.xpath('/html/body/div/div[@id="main"]/div[@id="content"]/section[@id="content-body"]/div[@id="topic"]/ul[@id="entry-item-list"]/li'):
         item = EksifeedItem()
         url_href = full_entry.xpath('footer/div[@class="info"]/a[@class="entry-date permalink"]/@href').extract_first()
         entry_link = str(url_href)

         item['url'] = urljoin("https://eksisozluk.com", url_href)
         item['entry'] = "\n ".join(full_entry.xpath('div[@class="content"]/text() | div[@class="content"]/a/text()').extract()).strip()
         item['author'] = full_entry.xpath('footer/div[@class="info"]/a[@class="entry-author"]/text()').extract()[0]
         item['date'] = full_entry.xpath('footer/div[@class="info"]/a[@class="entry-date permalink"]/text()').extract()[0]
         
         if not check_existence(entry_link):
            send_to_telegram('url: {0}\nentry: {1}\nyazar: {2}\ntarih: {3}\n'.format(item['url'], item['entry'], item['author'], item['date']))
      
         yield item
      

      # bu satırdan sonrası çok büyük ölçüde Eren Türkay'ın kodundan alıntıdır.
      # Eren Türkay'ın kodunu görmek için: https://github.com/eren/sozlukcrawler/blob/master/sozlukcrawl/spiders/eksisozluk.py
      current_page = int(response.xpath('/html/body/div[@id="container"]/div[@id="main"]/div[@id="content"]/section[@id="content-body"]/div[@id="topic"]/div[@class="clearfix sub-title-container"]/div[@class="pager"]/@data-currentpage').extract()[0])
      page_count = int(response.xpath('/html/body/div[@id="container"]/div[@id="main"]/div[@id="content"]/section[@id="content-body"]/div[@id="topic"]/div[@class="clearfix sub-title-container"]/div[@class="pager"]/@data-pagecount').extract()[0])

      current_url = response.request.url.split('?p')[0]

      next_page = current_page + 1
      if page_count >= next_page:
         yield Request('%s?p=%s' % (current_url, next_page))