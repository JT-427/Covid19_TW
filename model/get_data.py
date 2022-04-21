import pandas as pd
import datetime as dt

def get_data(start_date:dt.date=None, end_date:dt.date=None):
    if start_date == None:
        start_date = dt.date.today() - dt.timedelta(weeks=4)
    if end_date == None:
        end_date = dt.date.today()
    data = pd.read_csv('https://od.cdc.gov.tw/eic/covid19/covid19_tw_specimen.csv')
    data['通報日'] = pd.to_datetime(data['通報日'])
    data.set_index('通報日', inplace=True)
    if end_date >= dt.date.today():
        data = data.loc[start_date: end_date - dt.timedelta(days=1)]
    else:
        data = data.loc[start_date: end_date]

    return data