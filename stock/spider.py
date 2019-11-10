import os
import sys
import time
import argparse
import tushare as ts 


class Spider:
    def __init__(self):
        self.pro = ts.pro_api('95f7a4bf060e97230010a4287cf6db5a5e58c4deadef29f31d966978')

    def get_basic_data(self):
        basic_data = self.pro.stock_basic(exchange_id='', list_status='L', 
                fields='ts_code,symbol,name,area,industry,list_date')
        return basic_data
    
    def get_stock_code(self):
        basic_data = self.pro.stock_basic(exchange_id='', list_status='L', 
                fields='ts_code,symbol,name,area,industry,list_date')

        code_to_name = {}
        for _, row in basic_data.iterrows():
            code = row['ts_code'].split('.')[0]
            code_to_name[code] = row['name']

        return code_to_name

    def save_raw_data(self, basic_data, output):
        end_year = int(time.strftime("%Y", time.localtime())) + 2
        for idx, row in basic_data.iterrows():
            ts_code, name, list_date = row['ts_code'], row['name'], row['list_date']
            print('downloading {} {}...'.format(ts_code, name.encode('utf-8')))

            this_save_dir = os.path.join(output, ts_code + '_' + name)
            try:
                os.makedirs(this_save_dir)
            except:
                pass

            dates = []
            list_year = int(list_date[:4])
            for y in xrange(list_year, end_year):
                dates.append(str(y) + '0101')

            for i in xrange(len(dates) - 1):
                print('{}...'.format(dates[i]))
                df = ts.pro_bar(api=self.pro, 
                    ts_code=ts_code, 
                    asset='E', 
                    start_date=dates[i], 
                    end_date=dates[i + 1], 
                    freq='D', 
                    adj='hfq',)
                    #ma=[5, 10, 20, 40, 99, 250])

                this_save_name = dates[i] + '.csv'
                try:
                    df.to_csv(os.path.join(this_save_dir, this_save_name), index=False)
                except:
                    pass

                time.sleep(0.01)

    def get_report_data(self, year, quarter, topk=None):
        print ts.get_report_data(year, quarter)

    def get_profit_data(self, year, quarter, topk=None, 
            sort_fields=['roe', 'net_profit_ratio', 'business_income', 'bips', 'eps']):
        df = ts.get_profit_data(year, quarter)
        df.sort_values(by=sort_fields, ascending=False)

        if topk is None:
            return df
        else:
            return df.head(topk)

    def get_operation_data(self, year, quarter, topk=None, 
            sort_fields=['arturnover', 'inventory_turnover', 'currentasset_turnover']):
        df = ts.get_operation_data(year, quarter)
        df.sort_values(by=sort_fields, ascending=False)

        if topk is None:
            return df
        else:
            return df.head(topk)

    def get_growth_data(self, year, quarter, topk=None,
            sort_fields=['mbrg', 'nprg']):
        df = ts.get_growth_data(year, quarter)
        df.sort_values(by=sort_fields, ascending=False)

        if topk is None:
            return df
        else:
            return df.head(topk)

    def get_debtpaying_data(self, year, quarter, topk=None, 
            sort_fields=['cashratio', 'adratio']):
        df = ts.get_debtpaying_data(year, quarter)
        df.sort_values(by=sort_fields, ascending=False)

        if topk is None:
            return df
        else:
            return df.head(topk)

    def get_cashflow_data(self, year, quarter, topk=None,
            sort_fields=['cf_sales', 'cf_liabilities', 'cf_nm',]):
        df = ts.get_cashflow_data(year, quarter)

        df.sort_values(by=sort_fields, ascending=False)

        if topk is None:
            return df
        else:
            return df.head(topk)

    def get_stock_by_basic(self, year, quarter, topk):
        profit = self.get_profit_data(year, quarter, topk)
        profit_code = set(profit['code'])

        operation = self.get_operation_data(year, quarter, topk)
        operation_code = set(operation['code'])

        debt = self.get_debtpaying_data(year, quarter, topk)
        debt_code = set(debt['code'])

        cash = self.get_cashflow_data(year, quarter, topk)
        cash_code = set(cash['code'])

        return profit_code & operation_code & debt_code & cash_code




#  parser = argparse.ArgumentParser()
#  parser.add_argument('-t', '--type', type=str, help='operation type to do')
#  parser.add_argument('-o', '--output', type=str, required=True, help='output dir to save data')
#  args = parser.parse_args()

if __name__ == '__main__':
    #  op = args.type
    #  output_dir = args.output

    #  spider = Spider()
    #  print spider.get_profit_data(2018, 2)
    #  print spider.get_operation_data(2018, 2)
    #  print spider.get_debtpaying_data(2018, 2)

    #  stock_code = spider.get_stock_code()
    #  choosed_code = spider.get_stock_by_basic(2018, 3, 500)

    #  print '\n##############'
    #  for c in choosed_code:
    #      print c, stock_code[c]

    spider = Spider()
    basic_data = spider.get_basic_data()
    spider.save_raw_data(basic_data, 'raw_data')

