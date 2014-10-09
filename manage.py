# -*- coding: utf-8 -*-

from flask.ext.script import Manager
from bitcharts.database import manager as database_manager
from bitcharts.utils import get_ticker, search_key
from bitcharts import app, db, Exchange, Currency, Association


# @app.errorhandler(DatabaseError)
# def special_exception_handler(error):
#     return 'Database connection failed', 500

manager = Manager(app, with_default_commands=False)

manager.add_command('database', database_manager)


@manager.command
def get_values():
    """"""
    active_exchanges = Exchange.query.filter_by(active=True)

    active_currencies = [
        x.id for x in Currency.query.filter_by(active=True).all()
    ]

    active_exchanges_currencies = active_exchanges.filter(
        Exchange.currency_id.in_(active_currencies)
    ).all()

    for exchange in active_exchanges_currencies:
        print
        print exchange.name
        api_url = exchange.url + exchange.api
        req_json = get_ticker(api_url)
        # print req_json
        if req_json:
            key = exchange.key
            # print api_url
            # print exchange.key
            assoc = Association(
                exchange_id=exchange.id,
                currency_id=exchange.currency_id,
                last=search_key(req_json, key)
            )

            # print assoc.exchange_id
            # print assoc.currency_id
            # print type(assoc.last)
            if assoc.last:
                print assoc.last
                pass
                # db.session.add(assoc)
    # db.session.commit()


if __name__ == "__main__":
    manager.run()
