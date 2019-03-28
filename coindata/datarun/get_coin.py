#!/usr/bin/env python
import MySQLdb,re,sys,time

def mysql(sql):
    # import pdb;pdb.set_trace()
    dbhost = 'localhost'
    dbuser = 'root'
    dbpassword = '0871@YeJIa'
    db = 'coinData'
    try:    
        sqlconnect = MySQLdb.connect(dbhost,dbuser,dbpassword,db)
        cursor = sqlconnect.cursor()
    except:
        print "Failed to connect database"
        sys.exit(1)
    try:
        if not re.search(',,,',sql):
            sql_lower = sql.lower()
            res = cursor.execute(sql)
            if 'insert' in sql_lower:
                res = int(sqlconnect.insert_id())                    
            elif 'select' in sql_lower or 'desc' in sql_lower:
                res = cursor.fetchall()
            sqlconnect.commit()
            return res
        else:
            output = []
            for i in sql.split(',,,'):
                sql_lower = i.lower()
                res = cursor.execute(i)
                if 'insert' in sql_lower:
                    res = int(sqlconnect.insert_id())
                elif 'select' in sql_lower:
                    res = cursor.fetchall()
                output.append(res)
            sqlconnect.commit()
            return output
    except Exception as e:
        print str(e)
        sqlconnect.close()
        sys.exit(1)
    finally:
        sqlconnect.close()

def getData():
    sql = 'select distinct exchange from test;,,,select distinct baseCurrency from test;,,,select * from test;'
    ret = mysql(sql)
    basecurrency = [i[0] for i in ret[1]]
    exchange = [i[0] for i in ret[0]]
    data = {}
    for bc in basecurrency:
        data[bc] = {}
        for ex in exchange:
            data[bc][ex] = {}
    for row in ret[2]:
        if data[row[12]][row[11]]:
            j = 0
            for key in data[row[12]][row[11]].keys():
                if data[row[12]][row[11]][key][13] == row[13]:
                    if data[row[12]][row[11]][key][7] < row[7]:
                        data[row[12]][row[11]][key] = row
                    j=1
                    break
            if j == 0:
                data[row[12]][row[11]][row[13]] = row
        else:
            data[row[12]][row[11]][row[13]] = row
    for bc in basecurrency:
        for ex in exchange:
            if not data[bc][ex]:
                data[bc].pop(ex)
    #print data['omg']['bitfinex'].keys()
    #sys.exit(1)
    return data,basecurrency


def genWay(bc,qc):
    # try:
        # type(way)
    # except:
        # way = []
    # try:
        # type(way0)
    # except:
        # way0 = '' 
    if qc in basecurrency:
        for key in datapair[qc].keys():
            genWay(qc,key)
    else:
        print bc

    
# def genWay(bc):
    # try:
        # type(way)
    # except:
        # way = []
    # try:
        # type(way0)
    # except:
        # way0 = '' 
    # for qc in datapair[bc].keys():
        # way0 += ',%s' % datapair[bc][qc][1]
        # if qc in basecurrency and len(way) <=3:
            # print qc
            # way0 += ',%s' % genWay(qc)
        # way.append(way0)
        # way0 = ''
    # return way

def getDataWay():
    for bc in basecurrency:
        for qc in datapair[bc].keys():
            datapair[bc][qc] = 1

def getHighPair():
    #import pdb;pdb.set_trace()
    datapair = {}
    for bc in basecurrency:
        datapair[bc] = {}
        for ex in data[bc].keys():
            for qc in data[bc][ex].keys():
                try:
                    type(datapair[bc][qc])
                except:
                    datapair[bc][qc] = []
                datapair[bc][qc].append([round(data[bc][ex][qc][4]*(1-rate[ex]),float),'%s.%s' % (ex,bc),'%s.%s' % (ex,qc)])
        for qc in datapair[bc].keys():
            tmp = [i[0] for i in datapair[bc][qc]]
            datapair[bc][qc] = datapair[bc][qc][tmp.index(max(tmp))]
    return datapair


def main():
    global data,basecurrency,datapair
    data,basecurrency = getData()
    datapair = getHighPair()
    # print genWay('omg','eth') 
    print datapair['OMG']

    
            
if __name__ == '__main__':
    basecount = 1
    float = 8
    jump = 4
    rate = {"bitfinex":0.02,"hitbtc":0.02,"bittrex":0.01}
    main()