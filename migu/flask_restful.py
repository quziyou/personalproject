# -*- coding:utf-8 -*-

from flask import Flask, jsonify
from flask import request
from ordercailing import *
import json
import time

app = Flask(__name__)


@app.route('/miguorder/api/v1.0', methods=['GET'])
def ordermain():
    phone = request.args.get("phone")
    cmcc = request.args.get("cmcc")
    channel = request.args.get("channel")
    track = request.args.get("track")
    if not (phone and cmcc and channel and track):
        resCode = '100002'
        resMsg = '请传送正确的请求参数'
        return jsonify(resCode=resCode, phone=phone, cmcc=cmcc, channel=channel, track=track, resMsg=resMsg)

    else:
        proxy = get_proxy()
        proxies = {"http": "http://%s" % proxy}
        url_str = 'https://wawa.fm/static/isp3/cmcc_bak.html?&phone=%s&cmcc=%s&channel=%s&track=%s' %(phone, cmcc, channel, track)
        token, cookies = gettoken(phone, proxies)
        cookies, status_base = isopenbase(token, cookies, proxies)
        cookies, status_month = isopenmonth(token, cookies, proxies)
        if status_base == '1' and status_month == '1':
            resCode = '100001'
            resMsg = '该号码已是包月用户'
            return jsonify(resCode=resCode, phone=phone, cmcc=cmcc, channel=channel, track=track, resMsg=resMsg)
        else:
            resCode, resMsg = order_cailing(url_str, proxies)
            if resCode == '000000':
                time.sleep(2)
                migu6, cookies = cache_migu6(token, cookies, cmcc, proxies)
                migu7, cookies = cache_migu7(token, cookies, cmcc, proxies)
                if json.loads(migu7.split('(')[-1].replace(')', ''))['resCode'] == '301001':
                    resCode = '100003'
                    resMsg = '订购失败'
                    return jsonify(resCode=resCode, phone=phone, cmcc=cmcc, channel=channel, track=track, resMsg=resMsg)
                else:
                    migu8, cookies = cache_migu8(token, cookies, cmcc, proxies)
                    migu9, cookies = cache_migu9(token, cookies, cmcc, proxies)
                    migu10, cookies = cache_migu10(token, cookies, cmcc, proxies)
                    return jsonify(resCode=resCode, phone=phone, cmcc=cmcc, channel=channel, track=track, resMsg=resMsg, migu6=migu6, migu7=migu7, migu8=migu8, migu9=migu9, migu10=migu10)
            else:
                return jsonify(resCode=resCode, phone=phone, cmcc=cmcc, channel=channel,  track=track, resMsg=resMsg)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9896, threaded=True)
