# EkşiFeed

EkşiFeed, takip etmek istediğiniz başlıklardaki yeni entryleri Telegram mesajı olarak okumanızı sağlar. 

## Gerekenler

python3 kütüphaneleri:
* scrapy
* requests

Telegram'da yeni bot oluşturmanız gerekiyor. 
* Botfather ile sohbet ekranı başlatın.
* Botfather'a "/newbot" mesajı yollayın.
* Sorduğu soruları yanıtladıktan sonra size API key verecek. Bunu not edin.
* Botunuzla olan sohbet ekranını açın ve mesaj atın.
* https://api.telegram.org/bot[API_KEY]/getUpdates adresine gidip dönen cevaptaki "id" değerini not edin.

* Otomatize etmek için Heroku kullanabilirsiniz. (Heroku Scheduler eklemeniz gerekiyor.)
* Kendi makinelerinizi kullanıp cronjob yazarak otomatize edebilirsiniz.

## Kullanım

Repoyu indirdikten sonra ilk iş olarak /eksifeed/spiders/eksifeed_spider.py dosyasını açın ve aşağıda gösterilen satırlardaki yerlere daha önceden not ettiğiniz değerleri girin.
* `requests.get("https://api.telegram.org/bot[API_KEY]/sendMessage?chat_id=[CHAT_ID]&text={}".format(message))`
* `start_urls = ["[URL]",]`

Repo dizinindeyken `scrapy crawl eksifeed` komutu ile çalıştırın. 

![Ekran Görüntüsü](https://i.imgur.com/Kp8Qhmg.jpg)

## Not

eksifeed_spider.py'nin son satırları çok büyük ölçüde Eren Türkay'dan alıntıdır. (Dosyada neresi olduğu tam olarak yazıyor.)
[Eren Türkay'ın kodu](https://github.com/eren/sozlukcrawler/blob/master/sozlukcrawl/spiders/eksisozluk.py)
