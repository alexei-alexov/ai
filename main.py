from flask import Flask


app = Flask('ai')


import view

app.route('/')(view.base)
app.route('/genetic', methods=['GET', 'POST'])(view.genetic)