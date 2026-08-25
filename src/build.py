#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сборка index.html из template.html.
Подставляет все картинки из src/assets/ в HTML как base64 (data URI),
чтобы сайт оставался одним файлом без внешних зависимостей.

Запуск:  python3 build.py
Результат: ../index.html (перезаписывается)
"""
import base64, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'index.html')

html = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()

def repl(m):
    name = m.group(1)
    path = os.path.join(HERE, 'assets', name)
    ext = name.rsplit('.', 1)[1]
    mime = {'jpg': 'jpeg', 'png': 'png', 'webp': 'webp'}[ext]
    data = base64.b64encode(open(path, 'rb').read()).decode()
    return f'data:image/{mime};base64,{data}'

out = re.sub(r'\{\{([\w.\-]+)\}\}', repl, html)
leftover = re.findall(r'\{\{[\w.\-]+\}\}', out)
assert not leftover, f'Не найдены ассеты: {leftover}'
open(OUT, 'w', encoding='utf-8').write(out)
print('OK ->', os.path.abspath(OUT), round(os.path.getsize(OUT)/1024/1024, 2), 'MB')
