def sequences_generator(initial_key):
    '''Generates sequences of stored strings or sequences of kes or sequences of article tags'''

    SELSCTION_INPUT = '''укажите, что какие последовательности необходимо сгенерировать:
1) последовательность условий и результат;
2) последовательность ассоциированных норм;
3) последовательность ключей.
Введите число от 1 до 3, соответсвующее номеру варианта: '''

    db = shelve.open(db_default_adress, 'r')
    key_list = sorted(db.keys())
    initial_key_list = [x for x in key_list if 'init' in x]
    initial_key_counter = len(initial_key_list)

    selection_value = int(input(SELECTION_INPUT))

    if selection_value == 1:
        string_storage = []

        

    #unfinshed blueprint
    string_storage = []
    key_storage = []
    art_tag_storag = []
    while initial_key_counter > 0:
        iteration_counter = 0
        for i in range(len(db[initial_key_list[iteration_counter]]) - 1):
            string_storage.append([db[initial_key_list[iteration_counter]][i][0]])
            key_storage.append([db[initial_key_list[iteration_counter]][i][1]])
            key_storage.append([db[initial_key_list[iteration_counter]][i][2]])
        while True:
            pass
        initial_key_counter -= 1
        iteration_counter += 1
    
