# -*- coding: utf-8 -*-

import pymysql
import time
import sys


# 数据库连接函数
def connectdb():
    user = input('请输入数据库帐号：')
    passwd = input('请输入数据库帐号密码：')
    port = input('请输入数据库端口号：')
    host = 'localhost'
    db = 'personaldata'
    charset = 'utf8'
    conn = pymysql.connect(host=host, port=int(port), user=user, passwd=passwd, db=db, charset= charset)
    cursor = conn.cursor()
    return cursor, conn


# 密码本创建函数
def createCodebook():
    encryption = dict((v, k) for v, k in zip(range(len(words)),words))
    decryption = dict((v, k) for k, v in encryption.items())
    return encryption, decryption


# 加密函数
def doEncryption (text, num):
    wordList = []
    if num >= len(words):
        num = num % len(words)
    if len(words)> num >0:
        num = num
    if num <=0:
        num += len(words)
    for x in text:
        if x:
            if decryption[x] - num >= 0:
                wordList.append(encryption[decryption[x] - num])
            else:
                wordList.append(encryption[decryption[x] - num + len(words)])
        else:
            wordList.append('')
    encryptTex = ''.join(i for i in wordList)
    return encryptTex


# 解密函数
def doDecryption(text,num):
    wordList = []
    if num >= len(words):
        num = num % len(words)
    if num <len(words) and num >0:
        num = num
    if num <=0:
        num += len(words)
    for x in text:
        if decryption[x] + num <= len(words):
            wordList.append(encryption[decryption[x] + num])
        else:
            wordList.append(encryption[decryption[x] + num - len(words)])
    decryptTex = ''.join(i for i in wordList)
    return decryptTex


# 用户加密数字输入检测函数
def checkinput(num):
    i = 0
    while not num.isdigit():
        if i < 3:
            n = input('您的输入有误，您还有%s次机会,请输入一个整数：' % (3 - i))
            i += 1
        else:
            print('由于您多次错误输入，程序已退出……')
            sys.exit(1)
    return int(num)


# 帐号创建函数
def createaccount():
    account = input('请输入您要创建的帐号：')
    acc_passwd = input('请输入新帐号密码：')
    acc_num = input('请输入一个密码加密数字（必须为整数）：')
    acc_num = checkinput(acc_num)
    acc_passwd = doEncryption (acc_passwd, acc_num)
    print('请问是否需要创建支付密码：1.需要；0.不需要\n')
    userchoose = int(input())
    while userchoose !=1 and userchoose != 0:
        userchoose = int(input('您的输入有误，请按提示输入：1.需要；0.不需要\n'))
    if userchoose == 1:
        mon_passwd = input('请输入您的支付密码：')
        mon_num = input('请输入支付密码加密数字（必须为整数）：')
        mon_num = checkinput(mon_num)
        mon_passwd = doEncryption (mon_passwd, mon_num)
    elif userchoose == 0:
        mon_num = ''
        mon_passwd = ''
    category = input('请输账号类型：')
    url = input('请输入备忘url地址：')
    note = input('请输入帐号说明：')
    createtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    updatetime = createtime
    sql = '''INSERT INTO test(account, acc_passwd, mon_passwd, category, url, note, acc_num, mon_num, createTime, updateTime) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)'''
    values = [[account, acc_passwd, mon_passwd, category, url, note, acc_num, mon_num, createtime, updatetime]]
    cursor.executemany(sql, values)
    conn.commit()


# 查询帐号密码
def searchaccount():
    account = input('请输入您要查询的帐号：')
    note = input('请输入帐号说明：')
    try:
        cursor.execute('SELECT * FROM test WHERE account = %s AND note = %s', [account, note])
        data = cursor.fetchone()
        account = data[0]
        acc_num = int(data[6])
        acc_passwd = doDecryption(data[1], acc_num)
        mon_num = int(data[7])
        mon_passwd = doDecryption(data[2], mon_num)
        updatetime = data[-1]
        note = data[5]
        if mon_passwd == '':
            mon_passwd = '无'
        print('帐号：%s\n帐号密码：%s\n支付密码：%s\n帐号说明：%s\n帐号最后更新时间：%s' % (account, acc_passwd, mon_passwd, note, updatetime))
    except:
        print('查无此号……')


# 修改帐号密码：
def changepasswd():
    userchoose = int(input('请选择您要修改的密码类型：1.修改帐号密码；2.修改支付密码\n'))
    while userchoose != '1' or userchoose != '0':
        userchoose = int(input('请正确选择类型：1.修改帐号密码；2.修改支付密码\n'))
    while userchoose !=1 and userchoose != 0:
        userchoose = int(input('您的输入有误，请按提示输入：1.修改帐号密码；2.修改支付密码\n'))
    if userchoose == 1:
        account = input('请输入您要修改密码的帐号：')
        note = input('请输入该帐号说明：')
        acc_passwd = input('请输入新的帐号密码：')
        acc_num = input('请输入新的帐号密码加密数字（必须为整数）：')
        acc_num = checkinput(acc_num)
        acc_passwd = doEncryption (acc_passwd, acc_num)
        try:
            cursor.execute('UPDATE test SET acc_passwd = %s, acc_num = %s WHERE account = %s AND note = %s', [acc_passwd, acc_num, account, note])
            conn.commit()
        except:
            print('查无此号……')
    else:
        account = input('请输入您要修改密码的帐号：')
        note = input('请输入该帐号说明：')
        mon_passwd = input('请输入新的帐号密码：')
        mon_num = input('请输入新的帐号密码加密数字（必须为整数）：')
        mon_num = checkinput(acc_num)
        mon_passwd = doEncryption(acc_passwd, acc_num)
        try:
            cursor.execute('UPDATE test SET mon_passwd = %s, mon_num = %s WHERE account = %s AND note = %s',
                           [mon_passwd, mon_num, account, note])
            conn.commit()
        except:
            print('查无此号……')


# 删除帐号
def deleteaccount():
    account = input('请输入您要删除的帐号：')
    note = input('请输入该帐号说明：')
    try:
        cursor.execute('DELETE FROM test WHERE account = %s AND note = %s', [account, note])
        conn.commit()
        print('指定帐号已成功删除……')
    except:
        print('查无此号……')


if __name__ == '__main__':
    words = '''0OSHdK4>#i!a&8l%F/JT*?-u1;5W(BGzXVo|L~NA[nwY{)@2y+kP,`c]MICQb_67hj$r" s.v3qEptDf9U\\:RZ=}<gx^me'''
    encryption, decryption = createCodebook()
    try:
        cursor, conn = connectdb()
    except:
        print('数据库连接失败，程序已退出……')
        sys.exit(1)
    choose = input('请选择您的操作类型：\n1.创建新的帐号；2.查询帐号密码；3.修改帐号密码；4.删除已有帐号；5.退出系统\n')
    while choose not in ['1','2','3','4','5']:
        choose = input('请正确选择您的操作类型：\n1.创建新的帐号；2.查询帐号密码；3.修改帐号密码；4.删除已有帐号；5.退出系统\n')
    choose = int(choose)
    if choose == 1:
        createaccount()
    elif choose == 2:
        searchaccount()
    elif choose == 3:
        changepasswd()
    elif choose == 4:
        deleteaccount()
    else:
        sys.exit(0)
