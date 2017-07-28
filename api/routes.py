from flask_restful import Api

from resources.foo import Foo

api = Api()

api.add_resource(Foo,
        '/foo',
        '/foo/<int:foo_id>')
