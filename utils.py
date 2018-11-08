import re
import traceback


single_number = re.compile(r'\s*\d+')


def parse_matrix(data):
    try:
        graph = []
        lines = data.split('\r\n')
        for line in lines:
            row = []
            for number in single_number.finditer(line):
                row.append(int(number.group(0)))
            graph.append(row)
        return graph
    except Exception as error:
        print("Something went wrong. %s" % (error, ))
        traceback.print_exc()
        return None


def parse_config(data):
    try:
        config = {}
        for line in data.split('\r\n'):
            if not line:
                continue
            try:
                splitted = line.split(':', 1)
                key, value = splitted[0].strip(), splitted[1].strip()
                config[key] = value
            except IndexError:
                continue
        return config
    except Exception as error:
        print("Something went wrong. %s" % (error, ))
        traceback.print_exc()
        return None
