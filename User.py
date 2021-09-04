#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Database import users_counter, admins
from datetime import date

class User:

    need_agreement = False
    need_captcha = False
    need_sub_for_channel = False
    states = {"True": 1,
              "False": 0}

    def __init__(self, user_id):
        self.id = user_id
        self.__first_connect__()

    def __first_connect__(self):
        if users_counter.get_row("id", f"{self.id}") is None:
            adding_date = date.today()
            users_counter.add("id, date, accept_agreement, solve_captcha, subscribe_channel", f"{self.id}, '{adding_date}', 0, 0, 0")

    @property
    def users_amount(self):
        if users_counter.get_all_rows() is not None:
            return len(users_counter.get_all_rows())
        return 0

    @property
    def users_dict(self):
        return users_counter.get_all_rows()


    @property
    def is_accept_agreement(self):
        return True if users_counter.get_one_mean("accept_agreement", "id", f"{self.id}") == 1 else False

    @is_accept_agreement.setter
    def is_accept_agreement(self, new_state: bool):
        users_counter.set_mean("accept_agreement", f"{self.states[f'{new_state}']}", "id", f"{self.id}")

    @property
    def is_solve_captcha(self):
        return True if users_counter.get_one_mean("solve_captcha", "id", f"{self.id}") == 1 else False

    @is_solve_captcha.setter
    def is_solve_captcha(self, new_state: bool):
        users_counter.set_mean("solve_captcha", f"{self.states[f'{new_state}']}", "id", f"{self.id}")

    @property
    def is_subscribed_for_channel(self):
        return True if users_counter.get_one_mean("subscribe_channel", "id", f"{self.id}") == 1 else False

    @is_subscribed_for_channel.setter
    def is_subscribed_for_channel(self, new_state: bool):
        users_counter.set_mean("subscribe_channel", f"{self.states[f'{new_state}']}", "id", f"{self.id}")

    @property
    def status(self):
        if self.id not in admins:
            if self.is_accept_agreement is False and self.need_agreement is True:
                return False
            elif self.is_solve_captcha is False and self.need_captcha is True:
                return False
            elif self.is_subscribed_for_channel is False and self.need_sub_for_channel is True:
                return False
            else:
                return True
        else:
            return True
