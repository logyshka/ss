#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, User

def close():
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("✖ Закрыть", callback_data="close"))

def decline():
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("♨ Отмена", callback_data="close"))

def accept_agreement():
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("✅ Принять соглашение", callback_data="accept_agreement"))

def captcha(captcha_variants, captcha_solution):
    buttons = {}
    index = 1
    for captcha_variant in captcha_variants:
        buttons[index] = [f"{captcha_variant == captcha_solution}", captcha_variant]
        index += 1
    k = InlineKeyboardMarkup(row_width=4).add(
        InlineKeyboardButton(buttons[1][1], callback_data=f"captcha_solve_{buttons[1][0]}"),
        InlineKeyboardButton(buttons[2][1], callback_data=f"captcha_solve_{buttons[2][0]}"),
        InlineKeyboardButton(buttons[3][1], callback_data=f"captcha_solve_{buttons[3][0]}"),
        InlineKeyboardButton(buttons[4][1], callback_data=f"captcha_solve_{buttons[4][0]}")
    )
    return k

def sub_for_channel(channel_links):
    k = InlineKeyboardMarkup(row_width=1)
    for channel_link in channel_links:
        k.add(InlineKeyboardButton("📍 Канал", url=channel_link))
    k.add(InlineKeyboardButton("🤨 Проверить подписку", callback_data="check_sub_for_channel"))
    return k

def main_menu():
    return ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
        KeyboardButton("▶ Перевести в формат"),
        KeyboardButton("✳ Проверить валидность карты"),
        KeyboardButton("✳ Проверить BIN"))

def log_info(user: User):
    k = InlineKeyboardMarkup(row_width=1)
    if user.username is not None:
        return k.add(InlineKeyboardButton(f"id{user.id}", url=f"https://t.me/{user.username}"))
    else:
        return k.add(InlineKeyboardButton(f"id{user.id}", callback_data="d321dh_3489hd321s32"))