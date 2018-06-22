keys = ['Требования','Отсечка мотивировки','Начало мотивировки','Резолютивка']

def storer(global_store):
    local_store={}
    breaker = 1
    while breaker:
        for i in keys:
            local_store[i]=input("Введите '{}':\n".format(i))
        name = input("Введите реквизиты акта:\n")
        global_store[name]=local_store
        breaker = input("Введите 1, чтобы продолжить, или 0, чтобы закончить:\n")
