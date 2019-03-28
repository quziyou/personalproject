def getPass():
    import msvcrt
    print('请输入您的账号密码：', end='', flush=True)
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

if __name__ == '__main__':
    passwd = getPass()
    print(passwd)