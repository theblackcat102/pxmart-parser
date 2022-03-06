# Parse PX Mart grocery history from email (抓取全聯交易明細內容)

Parse purchase history from your gmail account and save into sqlite database. Useful for analyzing your local market inflation and recommending items to buy in your next purchase.

從你的郵箱抓出電子發票的明細，並將結果存為 sqlite 資料庫中。對於分析通膨與物品推薦有幫助。

## Setup

Install required package

```
pip install -r requirements.txt
```

Create table in your sqlite database

```
python -m modules.models 
```

[Follow this tutorial](https://towardsdatascience.com/automate-sending-emails-with-gmail-in-python-449cc0c3c317) to enable app login using app password.

Setup .env environment with app password access to your email account

```
EMAIL_ADDR="<Your email>"
EMAIL_PASS="<your app password>"
```

Run ingestion code, you should run this code periodically

```
python -m cli.ingest_purchase
```
