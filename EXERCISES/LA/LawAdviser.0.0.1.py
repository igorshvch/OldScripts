import re

def Main():
    '''Main function which starts the LawAdviser.py'''
    
    MAIN_INDICATOR_INPUT_PREFACE ='''Программа LawAdviser.
Главное Меню.
Введите:
"1", чтобы начать тестовый режим;
"2", чтобы начать режим редактора;
"0", чтобы выйти.
>> '''
    EDITOR_INDICATOR_INPUT_PREFACE ='''Введите соответсвующий код операции редактирования:
"1" - отредактировать запись в файле;
"2" - отредактировать(создать/удалить) файл в директории;
"3" - создать новый проект;
"9" - вернуться в Главное Меню;
"0" - выйти из программы.
>> '''
    
    main_indicator = int(input(MAIN_INDICATOR_INPUT_PREFACE))

    while main_indicator != 0:
        
        if main_indicator == 1:
            file_path = r'C:\Python34\EXERCISES\LA\Initiation.txt'
            test_indicator = 1
            while test_indicator != 0:
                lolines = Text_to_List(file_path)
                value_list = ValueExtract(lolines)
                code_list = CodeExtract(lolines)
                choise = Choises(value_list)
                file_path = Choise_Check(choise, code_list)
                if file_path == 'EMPTY':
                    print(r'Цепочка "вопрос - ответ" завершена, либо введено некорректное число')
                    print(r'Завершение программы')
                    test_indicator = 0
                    main_indicator = 0
                else:
                    continue
                
        elif main_indicator == 2:
            editor_indicator = int(input(EDITOR_INDICATOR_INPUT_PREFACE))
            while editor_indicator != 0:
                if editor_indicator == 1:
                    pass
                elif editor_indicator == 2:
                    pass
                elif editor_indicator == 3:
                    pass
                elif editor_indicator == 9:
                    pass
                
    print('-'*40)
    print(r'Сеанс завершен, до свидания!')


def Text_to_List(file_path):
    '''Unpacking a .txt file to list object'''
    
    with open(file_path) as f:
        list_of_lines = [line.rstrip('\n') for line in f.readlines()]
    return list_of_lines


def ValueExtract(list_of_lines):
    '''Extracting values from lines in list_of_lines file'''
    
    value_list =[]
    for i in list_of_lines:
        value_list.append(re.search(r'[^C]+', i).group()[:-1])
    value_list = list(enumerate(value_list, start = 1))
    return value_list


def CodeExtract(list_of_lines):
    '''Extracting cjdes from lines in list_of_lines file'''
    
    code_list = []
    for i in list_of_lines:
        code_list.append(re.search(r'(?<=C)\d+', i).group())
    code_list = list(enumerate(code_list, start = 1))
    return code_list


def Choises(value_list):
    '''Printing list object from Text_to_List
    and saving a choise made'''
    
    for line in value_list:
        i, statement = line
        print (i, ' - ', statement)
    choise = int(input(r'Выберите вариант ответа от 1 до %d: ' % len(value_list)))
    return choise


def Choise_Check(choise, code_list, indicator = 1):
    '''Finding the exact code for the choise input,
    then matches it to the corresponding URL'''

    file_path = 'EMPTY'
    for i in code_list:
        index, code = i
        if choise == index:
            code = str(code)
            with open(r'C:\Python34\EXERCISES\LA\URL_table.txt') as f:
                content = [line.rstrip('\n') for line in f.readlines()]
                for i in content:
                    if code in i:
                        file_path = re.search(r'(?<=URL)\S+', i).group()
    return file_path