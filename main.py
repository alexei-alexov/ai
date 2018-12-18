from flask import Flask


app = Flask('ai')
app.jinja_env.filters['zip'] = zip


import view

app.route('/')(view.base)
app.route('/ant', methods=['GET', 'POST'])(view.ant)
app.route('/genetic', methods=['GET', 'POST'])(view.genetic)
app.route('/qos')(view.qos)
app.route('/bigram')(view.bigram)
app.route('/art1', methods=['GET', 'POST'])(view.art1)