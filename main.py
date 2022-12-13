import os
import ast
import string
import importlib


def valid_function(data, isLower = True):
    letters = string.ascii_lowercase if isLower else string.ascii_uppercase

    if getattr(data, 'name')[0] not in letters:
        return False

    return True
    


def body_recourser(data, upper):
    result = True

    if hasattr(data, 'body'):
        for i in getattr(data, 'body'):
            if body_recourser(i, type(data)) is False:
                result = False
    
    return result


def module_resolver(module_path):
    isGood = True

    try:
        # result = __import__(modules_name_folder, globals(), locals(), [module_name])

        f = open(module_path, "r")

        data_file = f.read()
        
        result = ast.parse(data_file)

        f.close()

        for i in getattr(result, 'body', []):
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
    except Exception as e:
        isGood = False

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