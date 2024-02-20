# Домашнее задание к лекции 2. «Iterators. Generators. Yield»

import types


# 1.Итератор, для глубины вложенности списка = 2 (возвращает список элементов подряд - плоское представление)
class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list

    def __iter__(self):
        self.cnt = 0
        self.cnt_1 = 0
        self.elem = []
        return self

    def __next__(self):  
         
        if len(self.list_of_list) == self.cnt:
            raise StopIteration
        
        next_elem = self.get_next_elem()  
        
        return next_elem
        
    def get_next_elem(self):
        elem = self.list_of_list[self.cnt]
        
        if type(elem) is list:
            elem_2 = elem[self.cnt_1]
            self.cnt_1 += 1
            
            if len(elem) == self.cnt_1:
                self.cnt_1 = 0
                self.cnt +=1
                
        return elem_2
    
# 3.Итератор, для глубины вложенности списка = max_depth of python (возвращает список элементов подряд - плоское представление)
class FlatIterator_2:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list

    def __iter__(self):
        #print('start cycle')
        self.b_go = True
        self.cnt_list = 0
        self.cnt_stop = 0
        self.cnt_m = 0
        self.elem = []
        self.l_new = []
        return self

    def __next__(self):
        
        if self.b_go == True:  # Первый раз заходим в рекурсивную функцию распаковки списка, когда функция распаковки откроет крайнее вложение, self.b_go == False
            self.unpack_elem()  # отработав, она вернёт полностью распакованный список
            
        if len(self.list_of_list) == self.cnt_m:
            raise StopIteration
        
        # возвращаем элементы из распакованного списка
        next_elem = self.list_of_list[self.cnt_m]
        self.cnt_m +=1
        
        return next_elem
        
    # Функция распаковки
    def unpack_elem(self):
        
        if self.cnt_stop == len(self.list_of_list):  # Когда счётчик элементов НЕ явл.списком будет = длине списка, значит что мы распаковали всё и можем выйти из рекурсии
            self.b_go == False
            return self.list_of_list

        if len(self.list_of_list) == self.cnt_list:  # Достигнув длинны списка
            self.cnt_list = 0  # Обновляем счётчик для следующего распакованного списка
            self.cnt_stop = 0  # Счётчик остановки рекурсии, когда он будет равен длине списка, значит там распакованно всё
            self.list_of_list = self.l_new # обновляем наш список распакованным(первая глубина)
            self.l_new = []  # очищаем для дальнейшей записи распаковки следующего уровня
       
        self.elem = self.list_of_list[self.cnt_list]  # элемент из списка
        self.cnt_list += 1  # и сразу инкремент
        
        # Проверяем является ли элемент списком
        if isinstance(self.elem, list):
            self.l_new.extend(self.elem)  # если да, то добавляем его в конец l_new extend-ом - так раскрываются скобки(вложения)
        else:
            self.l_new.append(self.elem)  # если нет, то просто добавляем элементы в l_new
            self.cnt_stop += 1  # Инкремент для остановки рекурсии
            
        self.unpack_elem()  # рекурсия

    
# 2.Генератор, для глубины вложенности списка = 2 (возвращает список элементов подряд - плоское представление)
def flat_generator(list_of_lists):
    cnt_0 = 0
    cnt_1 = 0
    
    while len(list_of_lists) != cnt_0:
        elem = list_of_lists[cnt_0]
        if type(elem) is list:
            elem_2 = elem[cnt_1]
            cnt_1 += 1
            if len(elem) == cnt_1:
                cnt_1 = 0
                cnt_0 +=1
        yield elem_2

     
# 4.Генератор, для глубины вложенности списка = max_depth of python (возвращает список элементов подряд - плоское представление)
def flat_generator_2(list_of_list):
    nested = True  # Условие входа в цикл while
    
    while nested:  # Цикл будет, пока есть хоть один элемент isinstance(i, list)
        new = []  # очищаем распакованный n-уровня список
        nested = False  # Разрешение выхода из while
        for i in list_of_list:  
            if isinstance(i, list):
                new.extend(i)  # если да, то добавляем его в конец new extend-ом - так раскрываются скобки(вложения)
                nested = True  # Запрет выхода из while
            else:
                new.append(i)  # если нет, то просто добавляем элементы в new
        list_of_list = new  # Обновляем наш распакованный n-уровнем список для следующей итерации
    #return list_of_list  # return в отличии от yield не присваивает функции тип = генератор
    for i in list_of_list:  # для прохождения отладки по assert(type)
        yield i
    

def test_1():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    print('test_1 is done')
    
def test_2():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)
    print('test_2 is done')
    
def test_3():

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator_2(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator_2(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    print('test_3 is done')

def test_4():

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator_2(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        
        assert flat_iterator_item == check_item

    assert list(flat_generator_2(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    
    assert isinstance(flat_generator_2(list_of_lists_2), types.GeneratorType)
    print('test_4 is done')


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
    test_4()