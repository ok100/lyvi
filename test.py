# -*- coding: utf-8 -*-
def wrap(text, cols):
    wrapped_text = u''
    for line in text.split('\n'):
        try:
            line = unicode(line)
        except UnicodeDecodeError:
            line = unicode(line.encode('string_escape'))
        while len(line) > cols:
            wrapped_text += line[:cols - 2] + '->' + '\n'
            line = line[cols - 2:]
        wrapped_text += line + '\n'
    return wrapped_text[:-1]

str = '''Ой, как я выбегу, пробегу к ручью,
Вдоль, да по берегу.
Ой, как головушку светлую склоню
Над оберегами.
Тропою по ведам,
От сердца, да к небу
Рекою прольется песня моя!'''
print wrap(str, 10)
