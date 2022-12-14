import ast
import string

queue = []


def valid_function(data, isLower = True):
    letters = string.ascii_lowercase if isLower else string.ascii_uppercase

    if getattr(data, 'name', ' ')[0] not in letters:
        return False

    return True


def body_inspector(in_data):
    answer = True

    queue.append(in_data)

    while len(queue) > 0:
        raw_data = queue.pop(0)
        data = raw_data['data']
        come_from = raw_data['come_from']

        if type(data) in [ast.FunctionDef]:
            if come_from in [ast.ClassDef]:
                if not valid_function(data, True):
                    answer = False
            elif come_from in [ast.FunctionDef]:
                if not valid_function(data, False):
                    answer = False
        
        for i in getattr(data, "body", []):
            queue.append(
                {
                    "data": i,
                    "come_from": type(data),
                }
            )
    
    return answer


def module_resolver(module_path):
    result = True

    try:
        f = open(module_path, "r")

        data_file = f.read()
        
        result_parsing = ast.parse(data_file)

        f.close()
    except Exception:
        result = False
    
    result = result and body_inspector({
        "data": result_parsing,
        "come_from": ast.Module,
    })

    return 1 if not result else 0