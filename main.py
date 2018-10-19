from flask import Flask


app = Flask('ai')


import view

app.route('/')(view.base)