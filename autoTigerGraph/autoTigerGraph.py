import ijson

def get_first(filename):

    with open(filename, 'r') as f:
        objects = ijson.items(f, '', multiple_values=True, use_float=True)
        first  = objects.__next__()
        fields = list(zip(range(len(first)), 
                        list(first.keys()), 
                        [type(value).__name__ for value in first.values()]))

    return first, fields


def guess_vertex(json_object, vertex_name, guess_fields=None):

    if guess_fields == None:
        guess_fields = json_object.keys()
    
    type_translate = {'str': 'STRING', 'dict': 'STRING', 'float': 'DOUBLE', 
                      'bool': 'BOOL', 'int': 'INT'}

    gsql_cmd  = 'CREATE VERTEX ' + vertex_name + ' (PRIMARY_ID ' 
    
    for field in guess_fields:

        if field == 'date':
            gsql_cmd += 'date_time' + ' '
            gsql_cmd += 'DATETIME'
        else:    
            gsql_cmd += field + ' '
            gsql_cmd += type_translate[type(json_object[field]).__name__]
    
        gsql_cmd += ', '

    return gsql_cmd[:-2] + ')'


def problem_fields_to_str(json_object):

    for key, value in json_object.items():
        if isinstance(value, dict) or value == None:
            json_object[key] = str(value)
        if key == 'date':
            json_object.pop(key)
            json_object['date_time'] = value

    return json_object

def upsert_json(filename, conn, vertex_name, primary_id, n):

    ids = ['']*n
    bodies = ['']*n

    with open(filename, 'r') as f:
        objects = ijson.items(f, '', multiple_values=True, use_float=True)

        i = 0
        count = 0
        for json_object in objects:

            if json_object:
                ids[i]=json_object.pop(primary_id)
                bodies[i]=problem_fields_to_str(json_object)
                count += 1
                i += 1
                if i%n == 0:
                    conn.upsertVertices(vertex_name, list(zip(ids, bodies)))
                    i = 0

            else:
                break
                
    conn.upsertVertices(vertex_name, list(zip(ids[:i], bodies[:i])))

    return count


def create_vertex(shell, json_object, vertex_name, graph_name):

    print(shell.gsql('''
    drop graph {}
    drop vertex {}
    {}
    create graph {} (*)
    ls'''.format(graph_name,
                 vertex_name, 
                 guess_vertex(json_object=json_object, 
                                  vertex_name=vertex_name),
                 graph_name)))
