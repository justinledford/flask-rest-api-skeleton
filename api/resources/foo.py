from flask import jsonify, request
from flask_restful import Resource, abort

from common.util import abort_if_missing_parameters, jsonify
import models as m

class Foo(Resource):
    def get(self, foo_id):
        foo = m.Foo.query.get(foo_id)
        if not foo:
            abort(404, message='Foo %d not found' % foo_id)
        return jsonify(foo.to_dict())

    def post(self):
        required = ['name']
        abort_if_missing_parameters(required, request)
        data = request.get_json()
        if not data:
            abort(400, message='Invalid JSON')
        foo = m.Foo(**data)
        m.db.session.add(foo)
        return '', 201

    def delete(self, foo_id):
        foo = m.Foo.query.get(foo_id)
        foo.delete()
        return '', 200
