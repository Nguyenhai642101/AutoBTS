import json
import time
import datetime
from flask import Flask, render_template, request, jsonify, stream_with_context, Response
from download_data_from_firebase import *
from downloadCOT2 import *
from insert_data import *
from insert_data_2 import *
app = Flask(__name__)

import sqlite3


@app.route("/admin")
def getData():  # Retrieve data from database
    x, y, z, v, t = downloadData()
    info = {
        "Toadox": x,
        "Toadoy": y,
        "Toadoz": z,
        "Tocdogio": v,
        "Huonggio": t
    }
    # get_json = json.dumps(info)
    return jsonify(info)


# main route
@app.route("/")
def indexBegin():
    return render_template('indexBegin.html')


@app.route("/data_analysis")
def index():
    dummy_data = data_json()
    return render_template('indexBTS.html', matches=dummy_data.json)


@app.route('/data_json')
def data_json():
    dummy_data = [
        {
            "id": 1,
            "Name": "BTS1",
            "Location": "C1 - ĐHBK",
            "Coordinates": "(20.4213, 204.3211) ",
        },
        {
            "id": 2,
            "Name": "BTS2",
            "Location": "C2 - ĐHBK",
            "Coordinates": "(21.2452, 203.4953)",
        },
        {
            "id": 3,
            "Name": "BTS3",
            "Location": "C3-ĐHBK",
            "Coordinates": "(22.3454, 202.5324)",
        },
    ]
    return jsonify(dummy_data)

# @app.route('/Address')
# def address():
#     return render_template('indexAddress.html')

@app.route('/cot1')
def infor1():
    return render_template('index1.html')


@app.route('/cot2')
def infor2():
    return render_template('index2.html')

@app.route('/cot3')
def infor3():
    return render_template('index3.html')


@app.route('/chart-data')
def chart_data():
    def generate_data():
        while True:
            x, y, z, v, huonggio = downloadData()
            acc1, acc2, acc3, gyro1, gyro2, gyro3 = downloadDataElse()
            F = calculator()
            status1, statusNum = calculatorWarn()
            capgio = calculatorv()
            gocnghieng = calculatorDegree()
            insert_data_sql()
            json_data = json.dumps(
                {'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'speed': v,'capgio': capgio,
                 'huonggio':huonggio, 'gocnghieng': gocnghieng,
                 'F1': F[0], 'F2': F[1],'F3': F[2], 'F4': F[3], 'F5': F[4], 'F6': F[5],
                 'F7': F[6], 'F8': F[7], 'F9': F[8],
                 'x': x, 'y': y, 'z': z, 'status1': status1,'statusNum':statusNum,
                 'acc1': acc1, 'acc2': acc2, 'acc3': acc3,
                 'gyro1': gyro1, 'gyro2': gyro2, 'gyro3': gyro3})
            yield f"data:{json_data}\n\n"
            time.sleep(2)

    response = Response(stream_with_context(generate_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    # print(response)
    return response

@app.route('/dataCOT2')
def dataCOT2():
    def generate_data():
        while True:
            x, y, z, v, huonggio = downloadData2()
            acc1, acc2, acc3, gyro1, gyro2, gyro3 = downloadDataElse2()
            F = calculator2()
            status1, statusNum = calculatorWarn2()
            capgio = calculatorv2()
            gocnghieng = calculatorDegree2()
            insert_data_2()
            json_data = json.dumps(
                {'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'speed': v,'capgio': capgio,
                 'huonggio':huonggio, 'gocnghieng': gocnghieng,
                 'F1': F[0], 'F2': F[1],'F3': F[2], 'F4': F[3], 'F5': F[4], 'F6': F[5],
                 'F7': F[6], 'F8': F[7], 'F9': F[8],
                 'x': x, 'y': y, 'z': z, 'status1': status1,'statusNum':statusNum,
                 'acc1': acc1, 'acc2': acc2, 'acc3': acc3,
                 'gyro1': gyro1, 'gyro2': gyro2, 'gyro3': gyro3})
            yield f"data:{json_data}\n\n"
            time.sleep(2)

    response = Response(stream_with_context(generate_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    # print(response)
    return response


if __name__ == "__main__":
    app.run(debug=True, port=6868)
