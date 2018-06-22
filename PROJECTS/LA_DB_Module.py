import shelve
import random
import re

db_default_adress = r'PROJECTS\newdb'

#Main storages and mappings:
#random_part_string_id_storage --> set()
#string_id_storage --> set()
#string_id_to_string_mapping --> dict()
#article_tag_to_string_id_mapping --> dict()
#Should here be mentioned sequences of keys storage as a set object or as a mutable object?

with shelve.open(db_default_adress, 'c') as db_verification:
    if 'random_part_string_id_storage' not in db_verification.keys():
        db_verification['random_part_string_id_storage'] = set()
    if 'string_id_storage' not in db_verification.keys():
        db_verification['string_id_storage'] = set()
    if 'string_id_to_string_mapping' not in db_verification.keys():
        db_verification['string_id_to_string_mapping'] = dict()
    if 'article_tag_to_string_id_mapping' not in db_verification.keys():
        db_verification['article_tag_to_string_id_mapping'] = dict()


def db_generation_main():
    '''Generate a DB keys and values'''

    MAIN_MENU_OPTIONS_ENTRANCE = '''Добро пожаловать в мастер контента БД LawAdviser:
1)Создать новое значение;
2)Редактировать существущее значение.
3)Выход
Введите номер одной из предшествующих строк: '''

    MAIN_MENU_OPTIONS_LOOP = '''Какое действие следует выполнить следующим?
1)Создать новое значение;
2)Редактировать существующее значение;
3)Выйти из программы.
Введите номер одной из предшествующих строк:\n-->'''

    EXIT = 3 #Value here should be changed if the number of exit option is changed
    EXIT_STATEMENT = '''Спасибо, что воспользовались нашей програмой!
До свидания!'''

    main_menu_pointer = int(input(MAIN_MENU_OPTIONS_ENTRANCE))

    while main_menu_pointer != EXIT:
            if main_menu_pointer == 1:
                value_generator()
                main_menu_pointer = int(input(MAIN_MENU_OPTIONS_LOOP))
            elif main_menu_pointer == 2:
                value_editor()
                main_menu_pointer = int(input(MAIN_MENU_OPTIONS_LOOP))
            else: #some specification to user's input different than 3 is needed
                main_menu_pointer = EXIT

    print(EXIT_STATEMENT)


def value_generator():
    '''Generates key from user's input and accepts value defined by user'''

    KEY_INPUT = '''Пожалуйста, укажите значение ключа записи:\n-->'''
    STRING_INPUT = '''Пожалуйста, введите условие или результат, которые будут храниться по данному ключу (не используйте при вводе перенос строк!):\n-->'''
    REFERENCE_KEY_INPUT = '''Пожалуйста, введите ключ записи, на котрую необходимо проставить ссылку с введенного условия, либо нажмите Enter, в записи хранится конечный результат:\n-->'''
    ARTICLE_TAG_INPUT = '''Пожалуйста, введите статью и укажите ее подраздел, с котрым ассоциируется условие или реультат, либо нажмите Enter, чтобы оставить поле пустым:\n-->'''

    KEY_ERROR_MESSAGE = '''Введенное значение ключа уже исползуется. Пожалуйста, укажите значение ключа заново:\n-->'''
    REFERENCE_KEY_ERROR_MESSAGE = '''Ключ данной записи и ключ, на которы необходимо проставить ссылку, совпадают. Пожалуйста, введите другой ключ для ссылки:\n-->'''

    MENU_OPTIONS = '''Необходимо ли добавить еще данные в запись по заданному ключу? (Y = 1 / N = 0):\n-->'''

    db = shelve.open(db_default_adress, 'w')
    menu = True
    value_storage = []

    key = input(KEY_INPUT)
    while (key in db.keys()) == True:
        key = input(KEY_ERROR_MESSAGE)

    while menu == True:
        string = input(STRING_INPUT)

        ref_key = input(REFERENCE_KEY_INPUT)
        if ref_key == '':
            ref_key = 'fine'
        while ref_key == key:
            ref_key = input(REFERENCE_KEY_ERROR_MESSAGE)

        article_tag = input(ARTICLE_TAG_INPUT)

        value_storage.append([string, ref_key, article_tag])

        menu = int(input(MENU_OPTIONS))

    db[key] = value_storage
    db.close()

def value_editor():
    '''Editing values from existing keys'''

    INPUT_SELECTION = '''Ожидать ввода пользователем ключа записи, требующей редактуры, или предложить выбрать из имеющихся ключей? (Ввести = 1 / Выбрать = 0):\n-->'''
    KEY_USER_INPUT = '''Пожалуйста, введите ключ записи, которую необходимо редактировать:\n-->'''
    KEY_SELECTION = '''Пожалуйста, выберите номер ключа записи из таблицы ниже:\n'''
    STRING_SELECTION = '''Пожалуйста, укажаите номер строки, в которую необходимо внести изменения:\n-->'''
    TYPE_OF_VALUE_SELECTION = '''Пожалуйста, укажите номер значения, которое необходимо отредактировать (условие или результата = 0 / ключ ссылки = 1 / тэг нормы = 2):\n-->'''
    NEW_VALUE = '''Введите нужное значение:\n-->'''

    KEY_USER_INPUT_ERROR_MESSAGE = '''Введенный ключ отсутствует в базе данных. Пожалуйста, введите новое значение:\n-->'''

    MENU_OPTIONS = '''Необходимо ли отредактировать еще какую-либо запись? (Y = 1 / N = 0):\n-->'''

    db = shelve.open(db_default_adress, 'w')
    menu = True
    key_list = list(db.keys()).sort()

    while menu == True:
        input_selection = int(input(INPUT_SELECTION))
        if input_selection == 1:
            key = input(KEY_USER_INPUT)
            while key not in key_list:
                key = input(KEY_USER_INPUT_ERROR_MESSAGE)
        else:
            print(KEY_SELECTION)
            for (k, v) in enumerate(key_list):
                print(str(k) + '\t' + v)
            key_num = int(input('\n--> '))
            key = key_list[key_num]
        
        for (k, v) in enumerate(db[key]):
            print(str(k) + '\t' + v)

        list_item_number = int(input(STRING_SELECTION))
        for (k, v) in enumerate(db[key][list_item_number]):
            print(str(k) + '\t' + v)

        value_number = int(input(TYPE_OF_VALUE_SELECTION))
        new_value = input(NEW_VALUE)

        data = db[key]
        data[list_item_number][value_number] = new_value
        db[key] = data

        print('\nРезультат:\n' + str(db[key][list_item_number]))

        menu = int(input(MENU_OPTIONS))
    
    db.close()


def string_id_generator():
    '''Generates keys from article_tag value and randomly generated integer'''

    ARTICLE_INPUT = '''\nПожалуйста, введите ассоциируемую норму (в формате "статья:пункт/часть/абзац:пункт/подпункт:подпункт:абсолютный_номер_абзаца_в_норме:реквизиты_документа"):\n-->'''
    STRING_ID_TEST = '''\nПожалуйста, проверьте правильность введных реквизитов!\n'''
    TEST_QUESTION = '''\nРеквизиты верны? (Y = 1/ N = 0)\n-->'''

    db = shelve.open(db_default_adress, 'w')
    random_part_string_id_storage = db['random_part_string_id_storage']
    string_id_storage = db['string_id_storage']

    while True:
        random_part = (str(random.randint(0,9))
                       + str(random.randint(0,9))
                       + str(random.randint(0,9))
                       + str(random.randint(0,9))
                       + str(random.randint(0,9)))
        if random_part in random_part_string_id_storage:
            continue
        else:
            random_part_string_id_storage.add(random_part)
            break
        
    article_part = input(ARTICLE_INPUT)
    
    while True:
        article_splited = re.split('[:]', article_part)
        article_extended_form = ('Статья '
                                 + article_splited[0] + ' '
                                 + article_splited[-1] + '\n'
                                 + 'Структурные подразделы '
                                 + str(article_splited[1:-2]) + '\n'
                                 + 'абсолютный номер абзаца: '
                                 + str(article_splited[-2]))
        print(STRING_ID_TEST + '\n' + article_extended_form)
        check = int(input(TEST_QUESTION))
        if check == 1:
            break
        elif check == 0:
            article_part = input(ARTICLE_INPUT)
        else:
            print('\nВведено некорректное значение!')
            
    full_id = article_part + ':' + random_part

    string_id_storage.add(full_id)

    db['random_part_string_id_storage'] = random_part_string_id_storage
    db['string_id_storage'] = string_id_storage
    db.close()
    
    return full_id
