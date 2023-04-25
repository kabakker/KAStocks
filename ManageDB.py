from privateObjects import *
import os
import pymysql

class ManageDB:

    def __init__(self):
        self.db = local_db
        self.cursor = self.db.cursor()

    def create_stockprice_table(self):
        sql = "CREATE TABLE stock_prices_daily_adjusted (date DATE PRIMARY KEY)"
        self.cursor.execute(sql)
        self.db.commit()
        column_names = ["open", "high", "low", "close", "adjustedClose", "volume", "dividendAmount", "splitCoefficient"]
        for column_name in column_names:
            # Define the SQL query to create the column
            sql_query = f"ALTER TABLE stock_prices_daily_adjusted ADD {column_name} FLOAT"
            # Execute the query
            self.cursor.execute(sql_query)
            self.db.commit()

    #interval options: INTRADAY / INTRADAY_EXTENDED / DAILY / DAILY_ADJUSTED / WEEKLY / WEEKLY_ADJUSTED / MONTHLY / MONTHLY_ADJUSTED
    def get_time_series(self, interval):
        if not os.path.exists(interval):
            os.mkdir(interval)
        for stock_symbol in self.stock_symbol_list:
            stock_df = pd.read_csv("https://www.alphavantage.co/query?function=TIME_SERIES_"+interval+"&symbol="+stock_symbol+"&outputsize=full&datatype=csv"+"&apikey="+api_key)
            stock_df.to_csv(interval+"/"+stock_symbol+".csv")

    def search_stock(self, search_term):
        sql_query = f"SELECT * FROM sp500 WHERE Symbol LIKE '%{search_term}%' OR Security LIKE '%{search_term}%' OR `GICS Sector` LIKE '%{search_term}%' OR `GICS Sub-Industry` LIKE '%{search_term}%' OR `Headquarters Location` LIKE '%{search_term}%';"
        self.cursor.execute(sql_query)
        temp =  self.cursor.fetchall()
        return temp