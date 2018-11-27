from flask import Flask


app = Flask('ai')


import view

app.route('/')(view.base)
app.route('/genetic', methods=['GET', 'POST'])(view.genetic)
app.route('/qos')(view.qos)
app.route('/bigram')(view.bigram)
app.route('/art1', methods=['GET', 'POST'])(view.art1)