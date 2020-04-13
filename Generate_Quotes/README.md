## 名言を生成する

http://quotes.toscrape.com から名言をスクレイピングしてデータベースに保存しておいた.  
スクレイピングにはgo langを使用した.  

そのデータを使って、seq2seqモデルを用い、新たな名言を作成するデスクトップアプリを作った.  
(python app.py で実行できる)

### ファイル構成

                |----App/
                  |   |----models/
                  |   |----app.py
                  |   |----generate.py
                  |
                  |--Scraping/
                  |   |----scraping.go
                  |   |----test.db
                  |
                  |--Training/
                      |----trainig.py
                      |----utils.py

###実行画面

![](generate_quotes.png.png)
