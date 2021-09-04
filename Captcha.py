#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import listdir
from random import choice
from random import shuffle

def choose_captcha():
    captcha_folder = __file__.replace("\Bot\Captcha.py", "\Database\Captcha")
    captcha_list = listdir(captcha_folder)
    captcha = choice(captcha_list)
    captcha_file = f"{captcha_folder}\{captcha}"
    captcha_solution = captcha.replace(".png", "")
    captcha_variants = [captcha_solution]

    while len(captcha_variants) < 4:
        captcha_variant = [char for char in captcha_solution]
        shuffle(captcha_variant)
        captcha_variant = ''.join((i for i in captcha_variant))
        if captcha_variant != captcha_solution:
            captcha_variants.append(captcha_variant)

    return {"captcha_variants": captcha_variants,
            "captcha_solution": captcha_solution,
            "captcha_file": captcha_file}

