import os
import sys
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import easyocr
import traceback

app = Flask(__name__)

reader = easyocr.Reader(['pt','en'])

def gr(obj):
    val = obj
    if isinstance(obj, numpy.generic):
        val = obj.item()

    return round(val)

def g(obj):
    val = obj
    if isinstance(obj, numpy.generic):
        val = obj.item()

    return val

@app.route('/ocr_img', methods=["POST"])
def ocr_img():
    try:
        img = request.data
        output = reader.readtext(img)

        values = []
        for entry in output:
            pval = [[ [gr(x[0]),gr(x[1])] for x in entry[0]], entry[1], round(g(entry[2]) * 100,2)]
            values.append(pval)

        return jsonify({"output": values})
    except:
        traceback.print_exc()
        e = sys.exc_info()[0]
        print( "<p>Error: %s</p>" % e )

        return jsonify(
            {"error": "Did you mean to send: {'image_url': 'some_jpeg_url'}"}
        )

@app.route('/ocr', methods=["POST"])
def ocr():
    try:
        url = request.json['image_url']
        if url.endswith("jpg") or url.endswith("jpeg") or url.endswith("png"):
            output = reader.readtext(url)
    
            values = []
            for entry in output:
                pval = [[ [gr(x[0]),gr(x[1])] for x in entry[0]], entry[1], round(g(entry[2]) * 100,2)]
                values.append(pval)

            return jsonify({"output": values})
        else:
            return jsonify({"error": "only .png or.jpg files, please"})
    except:
        traceback.print_exc()
        e = sys.exc_info()[0]
        print( "<p>Error: %s</p>" % e )

        return jsonify(
            {"error": "Did you mean to send: {'image_url': 'some_jpeg_url'}"}
        )

if __name__ == '__main__':
    app.run()


