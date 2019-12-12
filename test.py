import requests as rq


def check_connect():
    resp = rq.post('http://127.0.0.1:6923')
    return resp.status_code


def check_method(req, test):
    if 'result' in req:
        print('test ' + test + ' passed', req['result'])
        return req['result']
    elif 'error' in req:
        print('test ' + test + ' has an error', req['error'])
    else:
        print(req)


def destroy_object(uuid):
    req = rq.post('http://127.0.0.1:6923', json={'jsonrpc': '2.0', 'method': 'bour.anal.Object.free', 'params': {'object': uuid}, 'id': 3}).json()
    if 'result' in req:
        print('object ' + uuid + ' destroyed')
    elif 'error' in req:
        print('Something went wrong', req)
    else:
        print(req)


def make_objects():
    req_echo = rq.post('http://127.0.0.1:6923', json={'jsonrpc': '2.0', 'method': 'echo', 'params': {'message': 'hello world!'}, 'id': 3}).json()
    check_method(req_echo, 'echo')
    req_server_version = rq.post('http://127.0.0.1:6923', json={'jsonrpc': '2.0', 'method': 'bour.anal.getServerVersionInfo', 'id': 1}).json()
    check_method(req_server_version, 'getServerVersionInfo')

    check_uid_on_server = rq.post('http://127.0.0.1:6923', json={'jsonrpc': '2.0', 'method': 'bour.anal.Object.isExists',
                                                                 'params': {'object': 'test_ctx_eval'},
                                                                 'id': 3
                                                                 }).json()
    res = check_method(check_uid_on_server, 'Object.isExists')
    if res:
        destroy_object('test_ctx_eval')

#EvaluationContext - working class

    req_object_create = rq.post('http://127.0.0.1:6923', json={'jsonrpc': '2.0', 'method': 'bour.anal.Object.create',
                                                                'params':
                                                                         {'className': 'EvaluationContext',
                                                                          # 'uuid': 'test_ctx_eval',
                                                                            'params': {
                                                                                'intensities': 'bla bla bla',
                                                                            }
                                                                         },
                                                                'id': 3
                                                                }).json()
    res = check_method(req_object_create, 'Object.create')

    check_uid_on_server = rq.post('http://127.0.0.1:6923', json={'jsonrpc': '2.0', 'method': 'bour.anal.Object.isExists',
                                                                 'params': {'object': res},
                                                                 'id': 3
                                                                 }).json()
    check_method(check_uid_on_server, 'Object.isExists')

    set_formula_into_class = rq.post('http://127.0.0.1:6923', json={'jsonrpc': '2.0', 'method': 'bour.anal.EvaluationContext.setFormula',
                                                                 'params': {'context': res,
                                                                            'expression': 'a0+a1*(A)+a2*(B/A)+a3*(A)'
                                                                            },
                                                                 'id': 3
                                                                 }).json()
    check_method(set_formula_into_class, 'EvaluationContext.setFormula')

    get_formula_into_class = rq.post('http://127.0.0.1:6923', json={'jsonrpc': '2.0', 'method': 'bour.anal.EvaluationContext.getFormula',
                                                                     'params': {'context': res,
                                                                                },
                                                                     'id': 3
                                                                     }).json()
    check_method(get_formula_into_class, 'EvaluationContext.getFormula')


def main():
    connect = check_connect()
    if connect == 200:
        make_objects()
    else:
        print('we have a connection error: ', connect)


if __name__ == '__main__':
    main()
