#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.types import Message, CallbackQuery, ContentType, ChatMember, Chat, InputFile
from aiogram.utils import executor
from User import User
from Bot.Captcha import choose_captcha
import Bot.MessageText as tx
import Bot.Keyboard as kb
from Database import admins

class TelegramBot:

    is_it_spam = False

    def __init__(self, bot_token, is_agreement=False, is_captcha=False, is_channel_sub=False,
                 channels_for_sub_id: set = ()):

        User.need_agreement = self.is_agreement = is_agreement
        User.need_captcha = self.is_captcha = is_captcha
        User.need_sub_for_channel = self.is_channel_sub = is_channel_sub
        self.channels_for_sub = channels_for_sub_id

        self.bot = Bot(token=bot_token, parse_mode="HTML")
        self.dis = Dispatcher(self.bot)
        self.user = None
        self.__start__()

    async def send(self, text: str, reply_markup=None):
        await self.bot.send_message(chat_id=self.user.id,
                                    text="<b><i>" + text + "</i></b>",
                                    reply_markup=reply_markup,
                                    parse_mode="HTML")

    async def edit(self, message_id, text, reply_markup=None):
        await self.bot.edit_message_text(chat_id=self.user.id,
                                         message_id=message_id,
                                         text="<b><i>" + text + "</i></b>",
                                         reply_markup=reply_markup,
                                         parse_mode="HTML")

    async def delete(self, message_id):
        await self.bot.delete_message(chat_id=self.user.id,
                                      message_id=message_id)

    async def handler_text(self, message: Message):
        pass

    async def handler_document(self, message: Message):
        pass

    async def handler_photo(self, message: Message):
        pass

    async def handler_audio(self, message: Message):
        pass

    async def handler_voice(self, message: Message):
        pass

    async def handler_callback(self, call: CallbackQuery):
        pass

    def __start__(self):
        @self.dis.message_handler(content_types=ContentType.TEXT)
        async def handler1(message: Message):
                self.user = User(message.from_user.id)
                if self.user.status:
                    if self.is_it_spam is True:
                        await self.Spam(message)
                    else:
                        if self.is_channel_sub is False:
                            await self.Access_is_true(message=message)
                        elif await self.Check_if_channel_member() is True:
                            await self.Access_is_true(message=message)
                        else:
                            self.user.is_subscribed_for_channel = False

                else:
                    if self.user.is_accept_agreement is False and self.is_agreement is True:
                        if "/start" == message.text:
                            await self.delete(message_id=message.message_id)
                            await self.send(text=tx.agreement,
                                            reply_markup=kb.accept_agreement())
                    elif self.user.is_solve_captcha is False and self.is_captcha is True:
                        if "/start" == message.text:
                            await self.delete(message_id=message.message_id)
                            captcha = choose_captcha()
                            with open(captcha["captcha_file"], "rb") as photo:
                                await self.bot.send_photo(photo=photo,
                                                          caption="<b><i>😘 Для использования бота пройди капчу\n⚠ Никакого ограничения по времени</i></b>",
                                                          reply_markup=kb.captcha(
                                                              captcha_variants=captcha["captcha_variants"],
                                                              captcha_solution=captcha["captcha_solution"]),
                                                          chat_id=self.user.id)

                    elif self.user.is_subscribed_for_channel is False and self.is_channel_sub is True:
                        if await self.Check_if_channel_member():
                            self.user.is_subscribed_for_channel = True
                        else:
                            channel_links = []
                            for channel_id in self.channels_for_sub:
                                channel: Chat = await self.bot.get_chat(chat_id=channel_id)
                                channel_link = await channel.get_url()
                                channel_links.append(channel_link)
                            await self.send(text="😘 Для использования бота подпишитесь на канал(ы)",
                                            reply_markup=kb.sub_for_channel(channel_links=channel_links))



        @self.dis.callback_query_handler(lambda call: True)
        async def handler2(call: CallbackQuery):
            self.user = User(call.from_user.id)

            if self.user.status:

                if self.is_channel_sub is False:
                    if "close" == call.data:
                        self.is_it_spam = False
                        await self.delete(call.message.message_id)
                    else:
                        await self.handler_callback(call=call)
                elif await self.Check_if_channel_member() is True and self.is_channel_sub is True:
                    if "close" == call.data:
                        await self.delete(call.message.message_id)
                    else:
                        await self.handler_callback(call=call)
                else:
                    self.user.is_subscribed_for_channel = False

            else:
                if self.user.is_accept_agreement is False and self.is_agreement is True:
                    if "accept_agreement" == call.data:
                        self.user.is_accept_agreement = True
                        await self.bot.answer_callback_query(call.id,
                                                             "✅ Соглашение успешно принято! Для продолжения введите /start",
                                                             show_alert=True)
                        await self.delete(call.message.message_id)

                elif self.user.is_solve_captcha is False and self.is_captcha is True:
                    if "captcha_solve_" in call.data:
                        result = call.data.replace("captcha_solve_", "").lower()
                        if result == "true":
                            self.user.is_solve_captcha = True
                            await self.bot.answer_callback_query(call.id,
                                                                 "✅ Капча успешно пройдена! Для продолжения введите /start",
                                                                 show_alert=True)
                            await self.delete(call.message.message_id)

                        elif result == "false":
                            captcha = choose_captcha()
                            await self.bot.answer_callback_query(call.id,
                                                                 "😔 Неправильно, попробуй ещё раз",
                                                                 show_alert=True)
                            await self.delete(call.message.message_id)
                            with open(captcha["captcha_file"], "rb") as photo:
                                await self.bot.send_photo(photo=photo,
                                                          caption="<b><i>😘 Для использования бота пройди капчу\n⚠ Никакого ограничения по времени</i></b>",
                                                          reply_markup=kb.captcha(
                                                              captcha_variants=captcha["captcha_variants"],
                                                              captcha_solution=captcha["captcha_solution"]),
                                                          chat_id=self.user.id)

                elif self.user.is_subscribed_for_channel is False and self.is_channel_sub is True:
                    if await self.Check_if_channel_member():
                        await self.bot.answer_callback_query(call.id,
                                                             "✅ Ты подписан на канал! Для продолжения введите /start",
                                                             show_alert=True)
                        await self.delete(call.message.message_id)

                    else:
                        await self.bot.answer_callback_query(call.id,
                                                             "😔 Не пытайся меня обмануть!",
                                                             show_alert=True)

        @self.dis.message_handler(content_types=ContentType.DOCUMENT)
        async def handler3(message: Message):
            self.user = User(message.from_user.id)
            if self.user.status:

                if self.is_channel_sub is False:
                    await self.handler_document(message)
                elif await self.Check_if_channel_member() is True:
                    await self.handler_document(message)
                else:
                    self.user.is_subscribed_for_channel = False

            else:
                if self.user.is_accept_agreement is False and self.is_agreement is True:
                    if "/start" == message.text:
                        await self.delete(message_id=message.message_id)
                        await self.send(text=tx.agreement,
                                        reply_markup=kb.accept_agreement())
                elif self.user.is_solve_captcha is False and self.is_captcha is True:
                    if "/start" == message.text:
                        await self.delete(message_id=message.message_id)
                        captcha = choose_captcha()
                        with open(captcha["captcha_file"], "rb") as photo:
                            await self.bot.send_photo(photo=photo,
                                                      caption="<b><i>😘 Для использования бота пройди капчу\n⚠ Никакого ограничения по времени</i></b>",
                                                      reply_markup=kb.captcha(
                                                          captcha_variants=captcha["captcha_variants"],
                                                          captcha_solution=captcha["captcha_solution"]),
                                                      chat_id=self.user.id)

                elif self.user.is_subscribed_for_channel is False and self.is_channel_sub is True:
                    if await self.Check_if_channel_member():
                        self.user.is_subscribed_for_channel = True
                    else:
                        channel_links = []
                        for channel_id in self.channels_for_sub:
                            channel: Chat = await self.bot.get_chat(chat_id=channel_id)
                            channel_link = await channel.get_url()
                            channel_links.append(channel_link)
                        await self.send(text="😘 Для использования бота подпишитесь на канал(ы)",
                                        reply_markup=kb.sub_for_channel(channel_links=channel_links))

        @self.dis.message_handler(content_types=ContentType.ANY)
        async def Spam(message: Message):
            self.user = User(message.from_user.id)
            await self.Spam(message)

        executor.start_polling(self.dis)

    async def Check_if_channel_member(self):
        for channel_for_sub in self.channels_for_sub:
            member: ChatMember = await self.bot.get_chat_member(chat_id=channel_for_sub,
                                                                user_id=self.user.id)
            if member.is_chat_member() or member.is_chat_admin() or member.is_chat_creator():
                continue
            return False
        return True

    async def Spam(self, message:Message):
        if self.is_it_spam is True and self.user.id in admins:
            try:
                if self.user.users_dict is not None:
                    for user in self.user.users_dict:
                        await self.bot.copy_message(chat_id=user["id"],
                                                    from_chat_id=message.chat.id,
                                                    message_id=message.message_id)
            finally:
                self.is_it_spam = False

    async def Access_is_true(self, message: Message):
        if self.user.id in admins:
            if message.text == "/bc":
                await self.delete(message_id=message.message_id)
                self.is_it_spam = True
                await self.send(text="Отправьте боту сообщение для рассылки", reply_markup=kb.decline())
            elif "/users" == message.text:
                await self.send(text=tx.users_amount(self.user.users_amount), reply_markup=kb.close())
                await self.delete(message_id=message.message_id)
            else:
                await self.handler_text(message=message)
        else:
            await self.handler_text(message=message)


