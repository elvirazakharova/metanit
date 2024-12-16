def plus():
    # Локальная область видимости функции `plus()`
    # Определим локальные переменные функции `plus()`
    plus_a = 5
    plus_b = 10
    print('Локальные переменные  функции `plus()`:', locals())
    def nested():
        """Вложенная функция `nested()`"""
        
        # локальная область видимости вложенной функции `nested()`
        # Здесь локальные переменные функции `plus()` ДОСТУПНЫ ТОЛЬКО ДЛЯ ЧТЕНИЯ
        
        print('=> Попытка изменить локальную переменную функции `plus()`')
        try:
            plus_a = plus_a + 1
        except UnboundLocalError:
            print('!!!Ошибка: UnboundLocalError (Локальное имя указано, но не привязано к значению)\n'
                  'Эта ошибка говорит о том, что локальную переменную `plus_a`, созданную во внешней '
                  'функции `plus()` НЕЛЬЗЯ ИЗМЕНИТЬ внутри вложенной функции nested()')
        finally:
            plus_a = 1
            # Здесь создалась новая локальная переменная функции `nested()`,
            # которая хранит свое значение только внутри функции `nested()`
            # и не имеет ни чего общего с локальной переменной plus_a, которая 
            # определялась ранее в локальной области видимости функции `plus()`
            print('plus_a =', plus_a, '=> создана новая локальная переменная '
                  'в области видимости функции `nested()`')
        
        # Укажем, что plus_b - не локальная, для вложенной функции `nested()`
        # !!! Нелокальные переменные должны существовать, т.е. должны быть 
        # определены в ближайшей (вышестоящей) области видимости)!
        nonlocal plus_b 
        print('Доступные переменные в функции `nested()`', locals())
        plus_b = plus_b + 10
        print(plus_b, '=> Переменная plus_b, локальной области функции plus(), '
              'изменена внутри области видимости вложенной функции `nested()`')

    # вызов вложенной функции `nested()` внутри функции `plus()`
    nested()
    
    print(plus_a, '=> Локальная переменная plus_a, созданная в функции '
          '`plus()` НЕ изменилась.')
    print(plus_b, '=> Локальная переменная plus_b, созданная в функции '
          '`plus()` изменена внутри вложенной функции nested()')

######################
# вызов функции plus()
plus()