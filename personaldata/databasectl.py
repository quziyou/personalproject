# -*- coding: utf-8 -*-

from texttable import Texttable
from Crypto.Cipher import AES
from Crypto import Random
import platform
import getpass
import pymysql
import base64
import random
import time
import sys


# 数据库连接函数
def connectdb():
    host = input('请输入数据库服务器IP：')
    port = int(input('请输入数据库端口号：'))
    user = input('请输入数据库帐号：')
    if platform_info == 'Linux':
        passwd = getpass.getpass('请输入数据库帐号密码：')
    elif platform_info == 'Windows':
        passwd = getPass()
    else:
        print('抱歉，本程序暂不支持您的操作系统！')
        sys.exit()
    db = input('请输入要连接的数据库名称：')
    table_name = input('请输入您要连接的数据表名称：')
    charset = 'utf8'
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd,
                           db=db, charset=charset)
    cursor = conn.cursor()
    return cursor, conn, table_name


# 密码输入星号展现，仅用于windows平台
def getPass():
    import msvcrt
    print('请输入数据库帐号密码：', end='', flush=True)
    li = []
    while True:
        ch = msvcrt.getch()
        # 回车
        if ch == b'\r':
            msvcrt.putch(b'\n')
            return b''.join(li).decode()
            break
        # 退格
        elif ch == b'\x08':
            if li:
                li.pop()
                msvcrt.putch(b'\b')
                msvcrt.putch(b' ')
                msvcrt.putch(b'\b')
        # ESC
        elif ch == b'\x1b':
            break
        else:
            li.append(ch)
            msvcrt.putch(b'*')
    return b''.join(li).decode()


# 检查帐号是否存在
def checkconnect(account, category):
    cursor.execute('''SELECT * FROM ''' + table_name + \
                   ''' WHERE account = %s AND category = %s''', [account, category])
    data = cursor.fetchone()
    return data


# 查询现有帐号
def searchaccounts(cursor, conn, table_name):
    cursor.execute(
        '''SELECT account, category, note FROM ''' +
        table_name +
        ''' group by account, category, note''')
    data = cursor.fetchall()
    table = Texttable()
    table.set_cols_align(['c', '1', 'l', 'l'])
    table.set_cols_valign(['m', 'm', 'm', 'm'])
    table.set_cols_dtype(['i', 't', 't', 't'])
    table.add_rows([['序号', '帐号', '帐号类型', '帐号说明']])
    for num, info in zip(range(len(data)), [x for x in data]):
        num = num + 1
        account = info[0]
        category = info[1]
        note = info[2]
        table.add_rows([['序号', '帐号', '帐号类型', '帐号说明'], [
                       num, account, category, note]])
    print(table.draw())


def searchinfo(account, category):
    try:
        cursor.execute('''SELECT * FROM ''' + table_name + \
                       ''' WHERE account = %s AND category = %s''', [account, category])
        data = cursor.fetchone()
    except BaseException:
        print('---------------------------')
        print('查无此号……')
    account = data[0]

    acc_passwd = data[1]
    if acc_passwd == '':
        acc_passwd = '无'
    else:
        acc_key = data[3]
        acc_AES = AESCipher(acc_key)
        acc_passwd = acc_AES.decrypt(acc_passwd).decode('utf-8')
    mon_passwd = data[2]
    if mon_passwd == '':
        mon_passwd = '无'
    else:
        mon_key = data[4]
        mon_AES = AESCipher(mon_key)
        mon_passwd = mon_AES.decrypt(mon_passwd).decode('utf-8')
    category = data[5]
    url = data[6]
    note = data[7]
    createtime = data[8]
    updatetime = data[-1]

    if url == '':
        url = '无'

    if note == '':
        note = '无'

    table = Texttable()
    table.set_cols_align(['l', 'l'])
    table.set_cols_valign(['m', 'm'])
    table.set_cols_dtype(['t', 't'])
    table.add_rows([['事项', '信息'], ['帐号', account], ['帐号密码', acc_passwd], ['支付密码', mon_passwd], [
                   '帐号类型', category], ['帐号说明', note], ['创建时间', createtime], ['最后更新', updatetime]])
    print(table.draw())


# 随机密码创建函数
def createPasswd():
    num = '0123456789'
    low_words = 'abcdefghijklmnopqrstuvwxyz'
    uper_words = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    specific_symbol = '!@#$%^&*()-=+;|,.:<>?'
    choices_num = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    choice = random.sample(choices_num, 4)
    while sum(choice) < 8 or sum(choice) > 16:
        choice = random.sample(choices_num, 4)
    passwd = ''.join(
        random.sample(
            num,
            choice[0]) +
        random.sample(
            low_words,
            choice[1]) +
        random.sample(
            uper_words,
            choice[2]) +
        random.sample(
            specific_symbol,
            choice[3]))
    passwd = ''.join(random.sample(passwd, len(passwd)))

    return passwd


# 创建AES加密算法类
class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, raw, num):
        raw = pad(raw, num)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]))


def pad(raw, num):
    raw = raw + (num - len(raw) % num) * chr(num - len(raw) % num)
    return raw


def unpad(raw):
    raw = raw[:-ord(raw[len(raw) - 1:])]
    return raw


def checknum(num):
    while num % 16 != 0:
        num = int(input('请输入密码加密长度（必须为16的倍数）：\n'))
    return num


# 帐号创建函数
def createaccount(table_name):
    table_name = table_name
    print('')
    print('+--------------------------------+')
    print('|  1.创建账号密码  2.返回主菜单  |')
    print('+--------------------------------+')
    userchoose = input('请选择您的下一步操作：')
    while userchoose not in ['1', '2']:
        userchoose = input('请正确选择您的下一步操作：')
    if userchoose == '1':
        print('')
        account = input('请输入您要创建的帐号：')
        print('+-----------------------------------+')
        print('|  1.手动输入密码  2.获取随机密码  |')
        print('+-----------------------------------+')
        userchoose2 = input('请选择密码生成方式：')
        while userchoose2 not in ['1', '2']:
            userchoose2 = input('请正确选择密码生成方式：')
        if userchoose2 == '1':
            acc_passwd = input('请输入新帐号密码：')
            while acc_passwd == '':
                acc_passwd = input('请务必输入您的新帐号密码：')
        elif userchoose2 == '2':
            acc_passwd = createPasswd()
            print('您的随机密码是：%s' % acc_passwd)
        passwd_num = int(input('请输入密码加密长度（如16、32、48……）：'))
        passwd_num = checknum(passwd_num)
        acc_key = input('请输入您的专用加密密钥(长度必须为16位)：')
        while len(acc_key) != 16:
            acc_key = input('加密密钥长度必须为16位：')
        acc_str = acc_key
        acc_AES = AESCipher(acc_key)
        acc_passwd = acc_AES.encrypt(acc_passwd, passwd_num)
        print('请问是否需要创建支付密码：1.需要；2.不需要：')
        userchoose = input()
        while userchoose not in ['1', '2']:
            userchoose = int(input('您的输入有误，请按上文提示输入：'))
        if userchoose == '1':
            print('+-----------------------------------+')
            print('|  1.手动输入密码  2.获取随机密码  |')
            print('+-----------------------------------+')
            userchoose3 = input('请选择密码生成方式：')
            while userchoose3 not in ['1', '2']:
                userchoose3 = input('请正确选择密码生成方式：')
            if userchoose3 == '1':
                mon_passwd = input('请输入您的支付密码：')
            elif userchoose3 == '2':
                mon_passwd = createPasswd()
                print('您的随机密码是：%s' % mon_passwd)
            passwd_num = int(input('请输入密码加密长度（如16、32、48……）：'))
            passwd_num = checknum(passwd_num)
            mon_key = input('请输入您的专用加密密钥(长度必须为16位)：')
            while len(mon_key) != 16:
                mon_key = input('加密密钥长度必须为16位：')
            mon_str = mon_key
            mon_AES = AESCipher(mon_key)
            mon_passwd = mon_AES.encrypt(mon_passwd, passwd_num)
        elif userchoose == '2':
            mon_passwd = ''
            mon_str = ''
        category = input('请输账号类型：')
        while category == '':
            category = input('请务必输账号类型：')
        url = input('请输入帐号对应url地址：')
        note = input('请输入帐号说明：')
        createtime = time.strftime('%Y-%m-%d %H:%M:%S',
                                   time.localtime(time.time()))
        updatetime = createtime
        sql = '''INSERT INTO ''' + table_name + \
            '''(account, acc_passwd, mon_passwd, acc_str, mon_str, category, url, note, createTime, updateTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        values = [[account, acc_passwd, mon_passwd, acc_str,
                   mon_str, category, url, note, createtime, updatetime]]
        cursor.executemany(sql, values)
        conn.commit()
        print('')
        print('----------------------------------')
        print('恭喜，您的新帐号密码已创建成功！')
    else:
        mainchannel(cursor, conn, table_name)
    print('')
    print('+----------------------------+')
    print('|  1.退出系统  2.返回主菜单  |')
    print('+----------------------------+')
    userchoose = input('请选择您的下一步操作：')
    while userchoose not in ['1', '2']:
        userchoose = input('请正确选择您的下一步操作：')
    if userchoose == '1':
        sys.exit(0)
    else:
        mainchannel(cursor, conn, table_name)


# 查询帐号密码
def searchaccount(table_name):
    table_name = table_name
    print('')
    print('+---------------------------------------------------------+')
    print('|  1.查询账号密码  2.查询现有帐号基本信息  3.返回主菜单  |')
    print('+---------------------------------------------------------+')
    userchoose = input('请选择您的下一步操作：')
    while userchoose not in ['1', '2', '3']:
        userchoose = input('请正确选择您的下一步操作：')
    if userchoose == '1':
        print('')
        account = input('请输入您要查询的帐号：')
        category = input('请输入帐号类型：')
        searchinfo(account, category)
    elif userchoose == '2':
        print('-----------------------------------------------------------------------------------')
        searchaccounts(cursor, conn, table_name)
    else:
        mainchannel(cursor, conn, table_name)
    print('')
    print('+----------------------------+')
    print('|  1.退出系统  2.返回主菜单  |')
    print('+----------------------------+')
    userchoose = input('请选择您的下一步操作：')
    while userchoose not in ['1', '2']:
        userchoose = input('请正确选择您的下一步操作：')
    if userchoose == '1':
        sys.exit(0)
    else:
        mainchannel(cursor, conn, table_name)


# 修改帐号密码：
def changepasswd(table_name):
    table_name = table_name
    print('')
    print('+--------------------------------------------------------------------------+')
    print('|  1.修改账户密码  2.修改支付密码  3.查询现有帐号基本信息  4.返回主菜单  |')
    print('+--------------------------------------------------------------------------+')
    userchoose = input('请选择您的下一步操作：')
    while userchoose not in ['1', '2', '3', '4']:
        userchoose = input('请正确选择您的下一步操作：')
    if userchoose == '1':
        print('')
        print('+------------------------------------------------+')
        print('|  1.修改账户密码  2.返回上级菜单  3.返回主菜单  |')
        print('+------------------------------------------------+')
        userchoose = input('请选择您的下一步操作：')
        while userchoose not in ['1', '2', '3']:
            userchoose = input('请正确选择您的下一步操作：')
        if userchoose == '1':
            print('')
            account = input('请输入您要修改密码的帐号：')
            category = input('请输入该帐号类型：')

            checkdata = checkconnect(account, category)
            while not checkdata:
                account = input('您输入的帐号、类型有误，请重新输入帐号：')
                category = input('请输入该帐号类型：')
                checkdata = checkconnect(account, category)

            print('')
            print('+-----------------------------------+')
            print('|  1.手动输入密码  2.获取随机密码  |')
            print('+-----------------------------------+')
            userchoose = input('请选择密码生成方式：')
            while userchoose not in ['1', '2']:
                userchoose = input('请正确选择密码生成方式：')
            if userchoose == '1':
                acc_passwd = input('请输入新帐号密码：')
            elif userchoose == '2':
                acc_passwd = createPasswd()
                print('您的随机密码是：%s' % acc_passwd)
            passwd_num = int(input('请输入密码加密长度（如16、32、48……）：'))
            passwd_num = checknum(passwd_num)
            acc_key = input('请输入您的专用加密密钥(必须为16位)：')
            if acc_key == '':
                cursor.execute('''SELECT acc_str FROM ''' + table_name +
                               ''' WHERE account = %s AND category = %s''', [account, category])
                data = cursor.fetchone()
                acc_key = data[0]
                acc_str = acc_key
                acc_AES = AESCipher(acc_key)
                acc_passwd = acc_AES.encrypt(acc_passwd, passwd_num)
            else:
                while len(acc_key) != 16:
                    acc_key = input('加密密钥必须为16位：')
                acc_str = acc_key
                acc_AES = AESCipher(acc_key)
                acc_passwd = acc_AES.encrypt(acc_passwd, passwd_num)
            updatetime = time.strftime(
                '%Y-%m-%d %H:%M:%S',
                time.localtime(
                    time.time()))
            try:
                cursor.execute(
                    '''UPDATE ''' +
                    table_name +
                    ''' SET acc_passwd = %s, acc_str = %s, updateTime = %s WHERE account = %s AND category = %s''',
                    [
                        acc_passwd,
                        acc_str,
                        updatetime,
                        account,
                        category])
                conn.commit()
                print('')
                print('-------------------------')
                print('恭喜，账户密码修改成功！')
            except BaseException:
                print('')
                print('--------------------')
                print('查无此号……')

        elif userchoose == '2':
            changepasswd()
        else:
            mainchannel(cursor, conn, table_name)
    elif userchoose == '2':
        print('')
        print('+------------------------------------------------+')
        print('|  1.修改支付密码  2.返回上级菜单  3.返回主菜单  |')
        print('+------------------------------------------------+')
        userchoose = input('请选择您的下一步操作：')
        while userchoose not in ['1', '2', '3']:
            userchoose = input('请正确选择您的下一步操作：')
        if userchoose == '1':
            print('')
            account = input('请输入您要修改支付密码的账户：')
            category = input('请输入该帐号说明：')
            checkdata = checkconnect(account, category)
            while not checkdata:
                account = input('您输入的帐号、类型有误，请重新输入帐号：')
                category = input('请输入该帐号类型：')
                checkdata = checkconnect(account, category)
            print('')
            print('+-----------------------------------+')
            print('|  1.手动输入密码  2.获取随机密码  |')
            print('+-----------------------------------+')
            userchoose = input('请选择密码生成方式：')
            while userchoose not in ['1', '2']:
                userchoose = input('请正确选择密码生成方式：')
            if userchoose == '1':
                mon_passwd = input('请输入新帐号支付密码：')
            elif userchoose == '2':
                mon_passwd = createPasswd()
                print('您的随机密码是：%s' % mon_passwd)
            passwd_num = int(input('请输入密码加密长度（如16、32、48……）：'))
            passwd_num = checknum(passwd_num)
            mon_key = input('请输入您的专用加密密钥(必须为16位)：')
            if mon_key == '':
                cursor.execute('''SELECT mon_str FROM ''' + table_name +
                               ''' WHERE account = %s AND category = %s''', [account, category])
                data = cursor.fetchone()
                mon_key = data[0]
                mon_str = mon_key
                mon_AES = AESCipher(mon_key)
                mon_passwd = mon_AES.encrypt(mon_passwd, passwd_num)
            else:
                while len(mon_key) != 16:
                    mon_key = input('加密密钥必须为16位：')
                mon_str = mon_key
                mon_AES = AESCipher(mon_key)
                mon_passwd = mon_AES.encrypt(mon_passwd, passwd_num)
            updatetime = time.strftime(
                '%Y-%m-%d %H:%M:%S',
                time.localtime(
                    time.time()))
            try:
                cursor.execute(
                    '''UPDATE ''' +
                    table_name +
                    ''' SET mon_passwd = %s, mon_str = %s, updateTime = %s WHERE account = %s AND category = %s''',
                    [
                        mon_passwd,
                        mon_str,
                        updatetime,
                        account,
                        category])
                conn.commit()
                print('')
                print('---------------------------')
                print('恭喜，支付密码修改成功！')
            except BaseException:
                print('')
                print('------------')
                print('查无此号……')
        elif userchoose == '2':
            changepasswd()
        else:
            mainchannel(cursor, conn, table_name)
    elif userchoose == '3':
        searchaccounts(cursor, conn, table_name)
    else:
        mainchannel(cursor, conn, table_name)
    print('')
    print('+----------------------------+')
    print('|  1.退出系统  2.返回主菜单  |')
    print('+----------------------------+')
    userchoose = input('请选择您的下一步操作：')
    while userchoose not in ['1', '2']:
        userchoose = input('请正确选择您的下一步操作：')
    if userchoose == '1':
        sys.exit(0)
    else:
        mainchannel(cursor, conn, table_name)


# 删除帐号
def deleteaccount(table_name):
    print('')
    print('+-----------------------------------------------------+')
    print('|  1.删除账号  2.查询现有帐号基本信息  3.返回主菜单  |')
    print('+-----------------------------------------------------+')
    userchoose = input('请选择您的下一步操作：')
    while userchoose not in ['1', '2', '3']:
        userchoose = input('请正确选择您的下一步操作：')
    if userchoose == '1':
        print('')
        account = input('请输入您要删除的帐号：')
        category = input('请输入该帐号类型：')
        checkdata = checkconnect(account, category)
        while not checkdata:
            account = input('您输入的帐号、类型有误，请重新输入帐号：')
            category = input('请输入该帐号类型：')
            checkdata = checkconnect(account, category)
        try:
            cursor.execute('''DELETE FROM ''' + table_name +
                           ''' WHERE account = %s AND category = %s''', [account, category])
            conn.commit()
            print('---------------------------')
            print('恭喜，指定帐号已成功删除！')
        except BaseException:
            print('------------')
            print('查无此号……')
    elif userchoose == '2':
        searchaccounts(cursor, conn, table_name)
    else:
        mainchannel(cursor, conn, table_name)
    print('')
    print('+----------------------------+')
    print('|  1.退出系统  2.返回主菜单  |')
    print('+----------------------------+')
    userchoose = input('请选择您的下一步操作：')
    while userchoose not in ['1', '2']:
        userchoose = input('请正确选择您的下一步操作：')
    if userchoose == '1':
        sys.exit(0)
    else:
        mainchannel(cursor, conn, table_name)


def mainchannel(cursor, conn, table_name):
    print('')
    print('+---------------------------------------------------+')
    print('|  1.创建新的帐号  2.查询帐号密码  3.修改帐号密码  |')
    print('|  4.删除已有帐号  5.退出系统                       |')
    print('+---------------------------------------------------+')
    choose = input('请选择您的操作类型：')
    while choose not in ['1', '2', '3', '4', '5']:
        choose = input('请正确选择您的操作类型：\n')
    choose = int(choose)
    if choose == 1:
        createaccount(table_name)
    elif choose == 2:
        searchaccount(table_name)
    elif choose == 3:
        changepasswd(table_name)
    elif choose == 4:
        deleteaccount(table_name)
    else:
        conn.close()
        sys.exit(0)


if __name__ == '__main__':
    platform_info = platform.system()
    try:
        cursor, conn, table_name = connectdb()
    except BaseException:
        print('数据库连接失败，程序已退出……')
        sys.exit(1)
    mainchannel(cursor, conn, table_name)
    conn.close()
