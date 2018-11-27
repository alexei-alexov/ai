from flask import render_template, request

import copy
import os
import utils
import random
from algorithms.genetic import search, evaluate_config
from algorithms.bigrams import generate_bigram, get_sentence, tokenize_text
from algorithms.art1 import ClusterPool, get_cluster_from_csv


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


def qos():
    return render_template('qos.html')


def bigram():
    # check data dump.
    context = {'error': None}
    try:
        text_file = open('static/bigram_src.txt', 'r')
        text = text_file.read()
        tokens = tokenize_text(text)
        print("tokens: ", tokens)
        print("TOKENS: ", list(map(list, tokens)))
        bigram = generate_bigram(copy.copy(tokens), tokenized=True)
        context['data'] = bigram
        context['text'] = text.replace('"', '\"')

        context['tokens'] = list({token.lower() for token_list in tokens for token in token_list})
        sentences_amount = request.form.get('sentences', 7)
        result = []
        for _ in range(sentences_amount):
            result.append(get_sentence(bigram))
        context['result'] = '<br>'.join(result)
    except Exception as error:
        print(error)
        import traceback
        traceback.print_exc()
        context['error'] = 'Could not find text file.'
    return render_template('bigram.html', **context)


def art1():
    context = {'error': None}
    pool = None
    if request.method == 'POST':
        try:
            csv_file = request.files.get('csv')
            try:
                beta = request.form.get('beta', '2')
                context['beta'] = beta
                if beta:
                    beta = int(beta)
            except Exception as error:
                raise ValueError('Wrong `beta` parameter!')
            try:
                rho = request.form.get('rho', '0.5')
                context['rho'] = rho
                if rho:
                    rho = int(rho)
            except Exception:
                raise ValueError('Wrong `rho` parameter!')
            #import ipdb; ipdb.set_trace()
            if csv_file:
                if not csv_file.filename:
                    raise ValueError('No file part!')
                if ('.' not in csv_file.filename or
                csv_file.filename.split('.')[-1].lower() != 'csv'):
                    raise ValueError('Wrong file!')
                print("GET CLUSTER FROM CSV. BETA: %s RHO: %s" % (beta, rho, ))
                pool, raw_data = get_cluster_from_csv(csv_file, beta, rho)
            else:
                raise ValueError("Choose CSV file to process.")
        except ValueError as error:
            context['error'] = str(error)
        except Exception as error:
            print(error)
            import traceback
            traceback.print_exc()
            context['error'] = 'Error processing file.'
    elif request.method == 'GET':
        pool = ClusterPool()
        V_SIZE = 10
        raw_data = [[round(random.random()) for _ in range(V_SIZE)] for _ in range(100)]
        for vector in raw_data:
                pool.add(vector)

    if pool:
        context['data'] = [cluster.data + [cluster.vector, ] for cluster in pool.clusters]
        context['raw_data'] = raw_data
    return render_template('art1.html', **context)