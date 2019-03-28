# -*- coding:utf-8 -*-

import config
from flask import request
from flask import Flask, jsonify
from dboperations.db import DbOperation


app = Flask(__name__)


@app.route('/proxy/query', methods=['GET'])
def proxy_query():
    db = DbOperation()
    params = request.args
    try:
        if params['count'] and int(params['count']) <= 5:
            infos = db.select(params.get('count', None), params)
            info_dict = {}
            for i in range(len(infos)):
                info_dict[i] = infos[i]
            json_result = jsonify(info_dict)
            return json_result
        else:
            return 'There is none!'
    except:
        return 'There is none!'


def start_api_server():
    app.run(host='0.0.0.0', port=config.API_PORT, threaded=True)


if __name__ == '__main__':
    start_api_server()
    