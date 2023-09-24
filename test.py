cookie = [b'view=cells; expires=Tue, 24 Oct 2023 16:59:55 GMT; path=/']


def modify_cookie(cookie):
    # Преобразование байтовой строки в строку
    cookie_str = cookie.decode('utf-8')
    
    # Разделение cookie на список пар ключ-значение
    cookie_pairs = cookie_str.split('; ')
    print(cookie_pairs)
    # Добавление значения "city" в cookie
    # modified_cookie = []
    # for pair in cookie_pairs:
    #     if pair.startswith('view='):
    #         # Если уже есть cookie с ключом "view", заменяем его значение
    #         modified_cookie.append('view=new_value')
    #     else:
    #         modified_cookie.append(pair)
    
    # # Преобразование списка обратно в строку cookie
    # modified_cookie_str = '; '.join(modified_cookie)
    
    # # Преобразование строки обратно в байтовую строку
    # modified_cookie_bytes = modified_cookie_str.encode('utf-8')
    
    # return modified_cookie_bytes
    
modify_cookie(cookie)