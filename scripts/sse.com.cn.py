import json
import httplib2
import sqlite3
import time
import sys

dt = time.strftime("%Y%m%d")
sqlite_file = 'sqlite/sse.com.cn.db'
url = 'http://yunhq.sse.com.cn:32041/v1/sh1/dayk/000001?select=date%2Copen%2Chigh%2Clow%2Cclose%2Cvolume%2Camount&begin=-2&end=-1'
sql = 'INSERT INTO szzs (dt,open,high,low,close,volume,amount) VALUES ("%s","%s","%s","%s","%s","%s","%s")'

if len(sys.argv) < 2:
    dt2 = time.strftime("%Y-%m-%d")
else:
    dt2 = sys.argv[1]
url2 = 'http://query.sse.com.cn/marketdata/tradedata/queryTradingByProdTypeData.do?searchDate=%s&prodType=gp' % dt2

def insert_sqlite(entries):
    conn = sqlite3.connect(sqlite_file)
    for entry in entries:
        d = str(entry[0])
        dat = d[0:4]+'-'+d[4:6]+'-'+d[6:8]
        sqli = sql % (dat,entry[1],entry[2],entry[3],entry[4],entry[5],entry[6])
        conn.execute(sqli)
    conn.commit()
    conn.close()

def parse_web():
    n = 0
    results = []
    print time.ctime() + ' -- ' + url
    while n < 10:
        n += 1
        try:
            http = httplib2.Http()
            response, content = http.request(url)
            c = json.loads(content)
            if dt == str(c['kline'][-1][0]):
                results = c['kline']
            n = 10
        except:
            print n
            time.sleep(60)
    return results

def insert_sqlite2(entries):
    tbs = {'12': 'shsc', '1': 'shag', '2': 'shbg'}
    conn = sqlite3.connect(sqlite_file)
    for entry in entries:
        sql = 'INSERT INTO %s (dt,sjzz,ltsz,cjl,cjje,cjbs,pjsyl,hsl) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s")' % (
               tbs[entry['productType']],dt2,entry['marketValue'],entry['negotiableValue'],entry['trdVol'],entry['trdAmt'],entry['trdTm'],entry['profitRate'],entry['exchangeRate'])
        conn.execute(sql)
    conn.commit()
    conn.close()

def parse_web2():
    n = 0
    results = []
    print time.ctime() + ' -- ' + url2
    while n < 10:
        n += 1
        try:
            http = httplib2.Http()
            headers = {'Referer': 'http://www.sse.com.cn/market/stockdata/overview/day/'}
            response, content = http.request(url2, 'GET', headers=headers)
            c = json.loads(content)
            if c['result'][0]['profitRate']:
                results = c['result']
            n = 10
        except:
            print n
            time.sleep(60)
    return results

def main():
    insert_sqlite(parse_web())
    insert_sqlite2(parse_web2())

if __name__ == '__main__':
    main()
