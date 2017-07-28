from contextlib import contextmanager
from functools import reduce
import os

from flask_sqlalchemy import SQLAlchemy, Model, BaseQuery
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

class Query(BaseQuery):
    """
    Extended Query class to provide a scalar values method
    """
    def values(self):
        """
        Return scalar values from a query

        Example:
            Rows:
            id name pass
            1  foo  ****
            2  bar  ****

        model.query.all().with_entities('name').values()
        ==
        ['foo', 'bar']
        """
        return [x for (x,) in self.all()]


db = SQLAlchemy(query_class=Query)

class BaseModel(Model):
    def delete(self):
        db.session.delete(self)
        db.session.flush()

    def update_fields(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self, columns=None, foreign=None):
        """
        Convert model to dictionary, can take columns
        to specify which columns to turn into key value pairs

        Also takes foreign columns, that can optionally
        be tuples to use a different key than the column
        """

        def _getattr(obj, attr):
            """
            getattr on nested objects
            """
            return reduce(getattr, attr.split('.'), obj)

        # Build dictionary of local columns
        if not columns:
            columns = [col.name for col in self.__table__.columns]
        d = {col: _getattr(self, col) for col in columns}

        # Build dictionary of foreign columns
        if foreign:
            for col in foreign:
                if type(col) == type(str()):
                    d[col] = _getattr(self, col)
                else:
                    _col, key = col
                    d[key] = _getattr(self, _col)

        return d

db.Model = db.make_declarative_base(BaseModel)

# Import all models so backrefs are created
from models.foo import Foo

# Session that can be used in a thread
@contextmanager
def thread_session():
    database_uri = \
        'mysql+pymysql://{}:{}@{}/{}'.format(
                *[os.environ.get(var) for var in \
                        ['DBUSER', 'DBPASS', 'DBHOST', 'DBNAME']])

    engine = create_engine(database_uri)
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)

    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
