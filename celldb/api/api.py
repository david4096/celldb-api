from klein import run, route
import numpy as np

from celldb import pd as celldb

import json
import csv
import io

URL = "localhost"

@route('/list_samples')
def list_samples(request):
    connection = celldb.connect(URL)
    return json.dumps({"sample_ids": list(celldb.list_samples(connection))})


@route('/list_features')
def list_features(request):
    connection = celldb.connect(URL)
    return json.dumps({"feature_ids": list(celldb.list_features(connection))})

@route('/matrix', methods=['POST'])
def matrix(request):
    connection = celldb.connect(URL)
    request_dict = json.loads(request.content.read())
    matrix_data = celldb.matrix(
        connection, request_dict['sample_ids'], request_dict['feature_ids'])
    ret_dict = {}
    for row in matrix_data:
        ret_dict[row[0]] = row[1:]
    return json.dumps({"matrix": ret_dict})

@route('/matrix/tsv', methods=['POST'])
def matrix_tsv(request):
    connection = celldb.connect(URL)
    request_dict = json.loads(request.content.read())
    df = celldb.df(
        connection, request_dict['sample_ids'], request_dict['feature_ids'])
    return df.to_csv(sep="\t")


@route('/matrix/dataframe', methods=['POST'])
def matrix_dataframe(request):
    connection = celldb.connect(URL)
    request_dict = json.loads(request.content.read())
    df = celldb.df(connection, request_dict['sample_ids'], request_dict['feature_ids'])
    return df.to_string()


@route('/matrix/html', methods=['POST'])
def matrix_html(request):
    connection = celldb.connect(URL)
    request_dict = json.loads(request.content.read())
    df = celldb.df(connection, request_dict['sample_ids'], request_dict['feature_ids'])
    return df.to_html()

def main(args=None):
    run("localhost", 8080)
