import ijson

print('Loaded local dev copy of autoTigerGraph!')

def get_first(filename):

    with open(filename, 'r') as f:
        objects = ijson.items(f, '', multiple_values=True, use_float=True)
        first  = objects.__next__()
        fields = list(zip(range(len(first)), 
                        list(first.keys()), 
                        [type(value).__name__ for value in first.values()]))

    return first, fields


def vertex_from_json(json_object, vertex_name, fields=None):

    if fields == None:
        fields = json_object.keys()
    
    type_translate = {'str': 'STRING', 'dict': 'STRING', 'float': 'DOUBLE', 
                      'bool': 'BOOL', 'int': 'INT'}

    gsql_cmd  = 'CREATE VERTEX ' + vertex_name + ' (PRIMARY_ID ' 
    
    for field in fields:

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


def upsert_json_vertices(filename, conn, vertex_name, primary_id, batch_size, max_verts):

    ids = ['']*batch_size
    bodies = ['']*batch_size

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
                if count >= max_verts:
                    break
                if i%batch_size == 0:
                    conn.upsertVertices(vertex_name, list(zip(ids, bodies)))
                    i = 0

            else:
                break
                
    conn.upsertVertices(vertex_name, list(zip(ids[:i], bodies[:i])))

    return count

def upsert_json_edges(filename, conn, from_name, from_field, edge_name, 
                      to_name, to_field, batch_size, max_edges, split_string=', '):

    froms = ['']*batch_size
    tos = ['']*batch_size

    with open(filename, 'r') as f:
        objects = ijson.items(f, '', multiple_values=True, use_float=True)

        i = 0
        count = 0
        for json_object in objects:

            if json_object:
                
                json_froms = json_object[from_field].split(split_string)
                jsom_tos = json_object[to_field].split(split_string)
                
                if len(json_from) > 1:
                    json_to *= len(json_form)
                elif len(json_to) > 1:
                    json_from *= len(json_to)
          
                for froms[i], tos[i] in zip(json_from, json_to):

                    count += 1
                    i += 1
                    if count >= max_edges:
                        break
                    if i%n == 0:
                        conn.upsertEdges(from_name, edge_name, to_name, list(zip(froms, tos)))
                        i = 0

            else:
                break

    return count
