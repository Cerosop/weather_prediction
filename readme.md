執行方法: 執行main.py後進入127.0.0.1:5000

main.py: 主程式，用來架設flask網站
templates/main.html: html
predict.py: 連接資料庫、以knn預測天氣、爬蟲抓取現在天氣
data.db: 儲存過去天氣資料
data.py: 將下載下來的csv檔存入data.db
csv: 放下載下來的csv檔
.env: 需要用到的套件