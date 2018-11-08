from flask import render_template, request

import copy
import utils
from algorithms.genetic import search, evaluate_config


def base():
    return render_template('base.html')


def genetic():
    context = {}
    if request.method == 'POST':
        graph = None
        if 'graph' in request.form and request.form['graph']:
            context['graph'] = request.form['graph']
            graph = utils.parse_matrix(request.form['graph'])
            context['graph_repr'] = repr(graph);
        config = None
        if 'search_config' in request.form and request.form['search_config']:
            context['search_config'] = request.form['search_config']
            config = utils.parse_config(copy.deepcopy(request.form['search_config']))
            if config:
                evaluate_config(config)
        results = search(graph, config)
        if results:
            context['winner'] = results[0]
            context['results'] = results
        else:
            context['error'] = "Something went wrong."

    return render_template('genetic.html', **context)