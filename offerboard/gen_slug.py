from time import time

from django.utils.text import slugify


def gen_slug(s):
    # Заменяем пробелы и преобразуем строку к нижнему регистру
    name = slugify(s, allow_unicode=True)

    translate = (
        ## Маленькие буквы
        # three-symbols
        (u"щ", u"sch"),
        # two-symbols
        (u"ё", u"yo"),
        (u"ж", u"zh"),
        (u"ц", u"ts"),
        (u"ч", u"ch"),
        (u"ш", u"sh"),
        (u"ы", u"yi"),
        (u"ю", u"yu"),
        (u"я", u"ya"),
        # one-symbol
        (u"а", u"a"),
        (u"б", u"b"),
        (u"в", u"v"),
        (u"г", u"g"),
        (u"д", u"d"),
        (u"е", u"e"),
        (u"з", u"z"),
        (u"и", u"i"),
        (u"й", u"j"),
        (u"к", u"k"),
        (u"л", u"l"),
        (u"м", u"m"),
        (u"н", u"n"),
        (u"о", u"o"),
        (u"п", u"p"),
        (u"р", u"r"),
        (u"с", u"s"),
        (u"т", u"t"),
        (u"у", u"u"),
        (u"ф", u"f"),
        (u"х", u"h"),
        (u"э", u"e"),
        (u"ъ", u""),
        (u"ь", u""),
    )
    # перебираем символы в таблице и заменяем
    for symb_in, symb_out in translate:
        name = name.replace(symb_in, symb_out)
    # возвращаем переменную
    return name + '-' + str(int(time()))