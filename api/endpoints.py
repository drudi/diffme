from bottle import request, response
from bottle import put, get
from base64 import b64decode
import pickle, json
from api.business import *
from api.exceptions import *

_version = '/v1'



@put(_version + '/diff/right')
def right_handler():
    data = None
    right = Right(RawData())
    try:
        data = b64decode(request.body.getvalue())
        right.put(data)
    except TypeError as e:
        print(e)
        response.status = 422
    response.status = 201
    response.set_header('Content-Type', 'application/json')
    return pickle.loads(data)

@put(_version + '/diff/left')
def left_handler():
    data = None
    left = Left(RawData())
    try:
        data = b64decode(request.body.getvalue())
        left.put(data)
    except TypeError as e:
        reponse.status = 422
    response.status = 201
    response.set_header('Content-Type', 'application/json')
    return pickle.loads(data)

@get(_version + '/diff')
def diff_handler():
    diff = Diff()
    response_data = None
    try:
        response_data = diff.getDiff()
    except NotFoundException as e:
        response.status = "404 %s" % e
    response.set_header('Content-Type', 'application/json')
    return response_data
