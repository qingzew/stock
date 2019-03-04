import datetime
import tushare as ts 

from base_obj import BaseObj
from logger import logger

from apscheduler.schedulers.blocking import BlockingScheduler

class TenPercent(BaseObj):
    def __init__(self):
        super(TenPercent, self).__init__()

    def is_two_days(self, st_data):
        """
        Args:
            st_data: stock price data in 10 consecutive days        

        return:
            whether the stock is ten percent in 2 consecutive days
        """
        # today
        open_price_0 = st_data.iloc[0, 2]
        high_price_0 = st_data.iloc[0, 3]
        low_price_0 = st_data.iloc[0, 4]
        close_price_0 = st_data.iloc[0, 5]
        pre_close_0 = st_data.iloc[0, 6]
        #change_0 = st_data.iloc[0, 7]
        pct_change_0 = st_data.iloc[0, 8]
        vol_0 = st_data.iloc[0, 9]

        # yestoday
        open_price_1 = st_data.iloc[1, 2]
        high_price_1 = st_data.iloc[1, 3]
        low_price_1 = st_data.iloc[1, 4]
        close_price_1 = st_data.iloc[1, 5]
        pre_close_1 = st_data.iloc[1, 6]
        #change_1 = st_data.iloc[1, 7]
        pct_change_1 = st_data.iloc[1, 8]
        vol_1 = st_data.iloc[1, 9]

        # the day before yesterday
        open_price_2 = st_data.iloc[2, 2]
        high_price_2 = st_data.iloc[2, 3]
        low_price_2 = st_data.iloc[2, 4]
        close_price_2 = st_data.iloc[2, 5]
        pre_close_2 = st_data.iloc[2, 6]
        #change_2 = st_data.iloc[2, 7]
        pct_change_2 = st_data.iloc[2, 8]
        vol_2 = st_data.iloc[2, 9]


        logger.debug('ts_code: {}'.format(ts_code))
        logger.debug('day0 open: {} high: {} low: {} close: {} pct: {} vol: {}'.format(
            open_price_0, high_price_0, low_price_0, close_price_0, pct_change_0, vol_0))
        logger.debug('day1 open: {} high: {} low: {} close: {} pct: {} vol: {}'.format(
            open_price_1, high_price_1, low_price_1, close_price_1, pct_change_1, vol_1))
        logger.debug('day2 open: {} high: {} low: {} close: {} pct: {} vol: {}'.format(
            open_price_2, high_price_2, low_price_2, close_price_2, pct_change_2, vol_2))

        if pct_change_0 > 0.98 and pct_change_1 > 0.98:
            logger.debug('====maybe this is the one====')

        if pct_change_0 > 0.98 and low_price_0 == close_price_0:
            if pct_change_1 > 0.98 and low_price_1 == close_price_1:
                #if pct_change_2 <= 0.98 and low_price_2 < high_price_2:
                    #if vol_0 < vol_1 and vol_1 < vol2:
                    #    return True
                if low_price_2 < high_price_2:
                    return True
        return False


    def get_10_percent(self):
        """
        Args:
        return:
            all the stocks is ten percent in 2 consecutive days  
        """
        pro = ts.pro_api('95f7a4bf060e97230010a4287cf6db5a5e58c4deadef29f31d966978')
    
        today = datetime.date.today()
        today = today.strftime('%Y%m%d')
        #n_days_before = datetime.date.today() - datetime.timedelta(days=10)
        #n_days_before = n_days_before.strftime('%Y%m%d')
        trade_cal = pro.trade_cal(exchange='', start_date='20190101', end_date=today)
        trade_cal = trade_cal[::-1]
        include_days = []
        for idx, row in trade_cal.iterrows():
            if row['is_open'] == 1:
                include_days.append(row['cal_date'])

            if len(include_days) == 10:
                break

        good_ts_codes = []
        for ts_code in self.ts_codes:
            df = ts.pro_bar(pro_api=pro, 
                ts_code=ts_code, 
                asset='E', 
                start_date=include_days[-1], 
                end_date=include_days[0], 
                freq='D',
                adj='qfq')

            try:
                #if self.is_two_days(df):
                #    good_ts_codes.append(ts_code)
                print ts_code, self.is_two_days(df)
            except Exception as e:
                print e


def job():
    print("Hello World")


if __name__ == '__main__':
    #tenper = TenPercent()
    #print tenper.get_10_percent()
    sched = BlockingScheduler()
    sched.add_job(job, 'cron', day_of_week='mon-sun', 
            hour=13, minute=05)
    sched.start()
