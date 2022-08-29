import os
from flask import Flask, request
from datetime import datetime
from dotenv import load_dotenv
import psycopg2
import pandas as pd


load_dotenv()
HOST = os.getenv("HOST")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("PASSWORD")
DB_NAME = os.getenv("DB_NAME")

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 200


@app.route('/crypto/', methods=['GET'])
def get_price():
    symbols = ["BTC", "ETH", "ETC", "XRP", "BNB"]
    symbol = request.args.get('symbol', default=None, type=str)
    year = request.args.get('year', default=datetime.today().year, type=str)
    month = request.args.get('month', default=datetime.today().month, type=str)
    date = request.args.get('date', default=datetime.today().day, type=str)
    hour = request.args.get('hour', default=None, type=str)
    
    if symbol == None:
      return "No symbol given", 400
    if symbol not in symbols:
      return f"Ticker '{symbol}' doesn't exist", 404
    if hour is None:
        return "Sepcifiy Open Hour"

    conn_string = f"postgresql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM \"public\".\"{symbol}\"")
    df = cur.fetchall()
    conn.commit()
    conn.close()
    cols = ["OpenTime", "Open", "High", "Low", "Close", "Volume", "CloseTime", 
            "QuoteAssetVolume", "NumTrades", "TakerBuyBaseAssetVolume", 
            "TakerBuyQuoteAssetVolume", "Ignore"]
    df = pd.DataFrame(df, columns=cols)
    dt = datetime(year, month, date, hour, 0)
    df[df['OpenTime'] == dt]
    return df["Open"]


if __name__ == '__main__':
    app.run(debug=True)
