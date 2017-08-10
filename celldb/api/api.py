import json

from klein import run, route
from twisted.web.static import File

from celldb import pd as celldb

URL = "localhost"


def set_acao(req):
    req.setHeader('Access-Control-Allow-Origin', '*')
    req.setHeader('Access-Control-Allow-Methods', '*')
    req.setHeader('Access-Control-Allow-Headers',
                  'x-prototype-version,x-requested-with')
    req.setHeader('Access-Control-Max-Age', 2520)  # 42 hours
    return req


@route('/static/', branch=True)
def static(request):
    return File("./static")


@route('/list_samples')
def list_samples(request):
    connection = celldb.connect(URL)
    request.setHeader('Content-Type', 'application/json')
    request.write(
        json.dumps({"sample_ids": list(celldb.list_samples(connection))}))
    request.finish()


@route('/list_features')
def list_features(request):
    connection = celldb.connect(URL)
    request.setHeader('Content-Type', 'application/json')
    request.write(
        json.dumps({"feature_ids": list(celldb.list_features(connection))}))
    request.finish()


@route('/matrix', methods=['POST'])
def matrix(request):
    connection = celldb.connect(URL)
    request_dict = json.loads(request.content.read())
    matrix_data = celldb.matrix(
        connection, request_dict['sample_ids'], request_dict['feature_ids'])
    ret_dict = {}
    for row in matrix_data:
        ret_dict[row[0]] = row[1:]
    request.setHeader('Content-Type', 'application/json')
    request.write(json.dumps({"matrix": ret_dict}))
    request.finish()


@route('/sparse_matrix', methods=['POST'])
def matrix_sparse(request):
    connection = celldb.connect(URL)
    request_dict = json.loads(request.content.read())
    matrix_data = celldb.sparse_dict(
        connection, request_dict['sample_ids'], request_dict['feature_ids'])
    request.setHeader('Content-Type', 'application/json')
    request.write(json.dumps(matrix_data))
    request.finish()


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
    df = celldb.df(
        connection, request_dict['sample_ids'], request_dict['feature_ids'])
    return df.to_string()


@route('/matrix/html', methods=['POST'])
def matrix_html(request):
    connection = celldb.connect(URL)
    request_dict = json.loads(request.content.read())
    df = celldb.df(
        connection, request_dict['sample_ids'], request_dict['feature_ids'])
    return df.to_html()


def main(args=None):
    run("localhost", 8080)
