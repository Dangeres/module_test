import ast
import string

queue = []


def valid_function(data, isLower = True):
    """
        Проверяет корректность названия функции.

        * params data - obj, объект проверки
        * params isLower - bool, флаг проверки первого символа, если True, значит проверяем первую букву на нижний регистр.

        return bool, результат проверки функции
    """

    letters = string.ascii_lowercase if isLower else string.ascii_uppercase

    if getattr(data, 'name', ' ')[0] not in letters:
        return False

    return True


def body_inspector(data):
    """
        Функция проверки каждого узла кода методом BFS.

        * params data - obj, начальный объект проверки

        return bool, результат глубокой проверки объекта
    """

    answer = True

    queue.append(data)

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
    """
        Главная функция проверки модуля.

        * params module_path - str, путь до модуля проверки

        return int[0, 1], результат проверки модуля
    """

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