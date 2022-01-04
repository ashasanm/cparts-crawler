import re

def clean_price(price):
    if price == '':
        return ''

    number = [string for string in price if string.isdigit()]
    number = int(''.join(number))
    
    return number


def clean_sold(sold):
    if sold == '':
        return ''

    number = [string for string in sold if string.isdigit()]
    number = int(''.join(number))
    
    return number


def is_desktop(title, category):
    title = title.lower()
    if category == "gpu":
        patterns = ['cd', 'driver','laptop', 'pc', 'mining', 'fan' , 'pendingin', 'kipas', 'bundle']
        for pattern in patterns:
            if re.search(pattern, title):
                print("Is not a Gpu=>", pattern, title)
                return False
        return True

    elif category == 'cpu':
        patterns = ['cd', 'driver','laptop', 'pc', 'mining', 'fan' , 
        'pendingin', 'kipas', 'sticker', 'stiker','gb', 'lenovo', 
        'hp', 'dell', 'macbook', 'apple', 'acer', 'asus', 'casing', 'case']
        for pattern in patterns:
            if re.search(pattern, title):
                print("Is not a Cpu=>", pattern, title)
                return False
        return True
    elif category == 'memory':
        patterns = ['hdd', 'ssd']
        for pattern in patterns:
            if re.search(pattern, title):
                print("Is not a Ram=>", pattern, title)
                return False
        return True
    elif category == 'case':
        patterns = ['gb', 'rakitan', 'harddisk', 'paket']
        for pattern in patterns:
            if re.search(pattern, title):
                print("Is not a Ram=>", pattern, title)
                return False
        return True
    else:
        return True