#!/usr/bin/env python
# -*- coding: utf-8 -*-

from re import findall
import sqlite3 as sq

db_path = __file__.replace("Databases.py", "db.db")

class Database:

    def __init__(self, table_name: str, columns: str):
        self.table = table_name
        self.table_columns = columns
        connection = sq.connect(db_path, check_same_thread=False)
        cursor = connection.cursor()
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name}({columns})')
        connection.commit()
        connection.close()

    def add(self, columns: str, means: str) -> None:
        try:
            connection = sq.connect(db_path, check_same_thread=False)
            cursor = connection.cursor()
            cursor.execute(f'INSERT INTO {self.table}({columns}) values({means})')
            connection.commit()
            connection.close()
        except Exception as e:
            print(e)

    def get_one_mean(self, need_column: str, column: str, mean: str) -> (int or str):

        connection = sq.connect(db_path, check_same_thread=False)
        cursor = connection.cursor()
        result = cursor.execute(f'select {need_column} from {self.table} where {column} is {mean}').fetchone()
        connection.commit()
        connection.close()
        if result is None:
            return None
        return result[0]

    def get_row(self, column: str, mean: str):
        result_dict = {}
        connection = sq.connect(db_path, check_same_thread=False)
        cursor = connection.cursor()
        result = cursor.execute(f'select * from {self.table} where {column} is {mean}').fetchone()
        index = 0
        try:
            for key in self.columns:
                result_dict[key] = result[index]
                index += 1
            return result_dict
        except:
            return None

    def get_all_rows(self) -> list[dict]:
        all_table = []
        connection = sq.connect(db_path, check_same_thread=False)
        cursor = connection.cursor()
        results = cursor.execute(f'select * from {self.table}').fetchall()
        connection.commit()
        connection.close()
        for result in results:
            result_dict = {}
            index = 0
            for key in self.columns:
                result_dict[key] = result[index]
                index += 1
            all_table.append(result_dict)
        return all_table

    def delete_row(self, column: str, mean: str):
        connection = sq.connect(db_path, check_same_thread=False)
        cursor = connection.cursor()
        cursor.execute(f'DELETE FROM {self.table} WHERE {column} is {mean}')
        connection.commit()
        connection.close()

    def set_mean(self, need_column: str, need_mean: str, column: str, mean: str):
        connection = sq.connect(db_path, check_same_thread=False)
        cursor = connection.cursor()
        cursor.execute(f'UPDATE {self.table} SET {need_column}={need_mean} WHERE {column}={mean}')
        connection.commit()
        connection.close()

    def get_sorted(self, sorted_by, selection: str = None):
        connection = sq.connect(db_path, check_same_thread=False)
        cursor = connection.cursor()
        if selection is None:
            selection = '*'
        result = cursor.execute(f'SELECT {selection} FROM {self.table} ORDER BY {sorted_by}').fetchall()
        connection.commit()
        connection.close()
        return result


    @classmethod
    def delete_table(cls, table_name: str) -> None:
        connection = sq.connect(db_path, check_same_thread=False)
        cursor = connection.cursor()
        cursor.execute(f'drop table {table_name}')
        connection.commit()
        connection.close()

    @property
    def columns(self):
        result = {}
        columns = findall(
            r"[A-Za-z_0-9]+ int|[A-Za-z_0-9]+ text|[A-Za-z_0-9]+ real|[A-Za-z_0-9]+ INT|[A-Za-z_0-9]+ TEXT|[A-Za-z_0-9]+ REAL",
            self.table_columns)
        for column in columns:
            column = column.split(' ')
            column_name = column[0]
            column_type = column[1].lower()
            if column_type == 'text':
                result[column_name] = 'nothing'
            elif column_type == 'int':
                result[column_name] = 0
            elif column_type == 'real':
                result[column_name] = 0.0
        return result
