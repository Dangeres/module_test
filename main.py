import os
import ast
import string
import importlib


def valid_function(data, isLower = True):
    letters = string.ascii_lowercase if isLower else string.ascii_uppercase

    if getattr(data, 'name', ' ')[0] not in letters:
        return False

    return True


queue = []


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
    isGood = True

    try:
        # result = __import__(modules_name_folder, globals(), locals(), [module_name])

        f = open(module_path, "r")

        data_file = f.read()
        
        result_parsing = ast.parse(data_file)

        f.close()
    except Exception as e:
        isGood = False

    if False:
        for i in getattr(result_parsing, 'body', []):
            if type(i) == ast.FunctionDef:
                if not valid_function(i, False):
                    isGood = False

                    break
            
            elif type(i) == ast.ClassDef:
                for j in getattr(i, 'body'):
                    if type(j) == ast.FunctionDef:
                        if not valid_function(j, True):
                            isGood = False

                            break
    
    isGood = isGood and body_inspector({
        "data": result_parsing,
        "come_from": ast.IsNot,
    })

    # print(1 if not isGood else 0)
    # print(1 if not  else 0)

    return 1 if not isGood else 0


def main():
    modules_name_folder = 'modules'

    modules_name = os.listdir(modules_name_folder)

    for module_name in modules_name:
        if not module_name.endswith('.py'):
            continue

        clear_name_module = module_name.rsplit('.', 1)[0]
        
        result_method_check = module_resolver(f"{modules_name_folder}/{module_name}")
        

        print(f'module {module_name} is {result_method_check}')


if __name__ == '__main__':
    main()