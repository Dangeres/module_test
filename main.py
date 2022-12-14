import os
import resolve


def main():
    modules_name_folder = 'modules'

    modules_name = os.listdir(modules_name_folder)

    for module_name in modules_name:
        if not module_name.endswith('.py'):
            continue

        clear_name_module = module_name.rsplit('.', 1)[0]
        
        result_method_check = resolve.module_resolver(f"{modules_name_folder}/{module_name}")
        

        print(f'module {module_name} is {result_method_check}')


if __name__ == '__main__':
    main()