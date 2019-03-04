import tushare as ts 
from logger import logger

class BaseObj(object):
    def __init__(self):
        self.pro = ts.pro_api('95f7a4bf060e97230010a4287cf6db5a5e58c4deadef29f31d966978')

        self.basic_datas = self.pro.stock_basic(exchange_id='', list_status='L', 
                fields='ts_code,symbol,name,area,industry,list_date')
    
        self.ts_codes = []
        for _, row in self.basic_datas.iterrows():
            code = row['ts_code']
            self.ts_codes.append(code)


if __name__ == '__main__':
    bo = BaseObj()


