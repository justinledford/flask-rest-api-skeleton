import flask.json
from flask_restful import abort

from stringcase import snakecase, camelcase

def abort_if_missing_parameters(required_params, request):
    keys = request.json.keys()
    for param in required_params:
        if param not in keys:
            abort(400, message='Missing parameters')


def convert_keys(d, case):
    """
    Convert all keys of a dict from snake to camel, or camel to snake.
    """
    if not d:
        return

    if case == 'camel':
        f = camelcase
    elif case == 'snake':
        f = snakecase
    else:
        raise ValueError('Case type must be either "snake" or "camel"')

    if type(d) == type([]):
        for e in d:
            e = convert_keys(e, case)
    elif type(d) == type({}):
        keys = list(d.keys())
        for k in keys:
            if type(d[k]) == type({}):
                d[k] = convert_keys(d[k], case)
            elif type(d[k]) == type([]):
                for e in d[k]:
                    e = convert_keys(e, case)
            d[f(k)] = d.pop(k)
    return d


def jsonify(*args, **kwargs):
    """
    Wrapper for Flask's jsonify to convert keys from snake to camelcase
    """
    if len(args) == 1 and isinstance(args[0], (list, dict)):
        return convert_keys(args[0], 'camel')

    return flask.json.jsonify(args, kwargs)
