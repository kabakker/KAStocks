from privateObjects import *
import os
import pymysql

class ManageDB:

    def __init__(self):
        self.db = local_db
        self.cursor = self.db.cursor()

    def create_stockprice_table(self):
        column_names = ["IBM", "TSLA", "AAPL", "MSFT", "AMZN"]
        sql = "CREATE TABLE stock_prices (id INT AUTO_INCREMENT PRIMARY KEY, date DATE)"
        self.cursor.execute(sql)
        self.db.commit()

        for column_name in column_names:
            # Define the SQL query to create the column
            sql_query = f"ALTER TABLE stockprices ADD {column_name} VARCHAR(255)"

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


db = ManageDB()
db.create_company_info_table()