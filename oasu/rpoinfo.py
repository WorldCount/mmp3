#!/usr/bin/env python
# -*- coding: utf-8 -*-

from grab import Grab
from grab.error import (GrabTimeoutError, GrabAuthError)
from .errors import *
from datetime import datetime

__author__ = 'WorldCount'

"""
Получение информации по ШПИ в ОАСУ
"""


# Получает данные в ОАСУ по ШПИ
class RpoInfo:

    # Конструктор
    def __init__(self, login='post', password='stat', auth=True):

        # Информация по отправлению
        self.__info = ''
        self.__barcode = ''
        self.__data = ''
        # Логин и пароль
        self.__login = login
        self.__password = password
        # Настройки соединения
        self.__connect_timeout = 5
        self.__timeout = 5
        # Ссылки
        self.__url = 'http://vinfo.russianpost.ru'
        self.__oasu_url = '%s/servlet/user?action=login&login=%s&password=%s&submit=OK'
        self.__auth_url = self.__oasu_url % (self.__url, self.__login, self.__password)
        self.__parse_url = '%s/servlet/track_post_item?barCode=%s&action=search&searchType=barCode&show_form=yes'
        # Парсер
        self.__grab = Grab()
        self.__grab.setup(connect_timeout=self.__connect_timeout, timeout=self.__timeout)

        if auth:
            self.__authorization()

    # Запрос
    def __query(self, url):
        try:
            self.__grab.go(url)
        except GrabTimeoutError:
            raise OasuTimeoutError()
        except GrabAuthError:
            raise OasuAuthError()

    # Авторизация на сайте
    def __authorization(self):
        self.__query(self.__auth_url)

    # Парсит данные по ссылке
    def __parse(self, url):
        self.__query(url)
        return self.__grab.doc.select('//body/table/tr[@valign="top"]')

    # Получает информацию по ШПИ
    def check_num(self, barcode):
        self.__info = ''
        self.__data = []
        self.__barcode = barcode
        # Ищем в ОАСУ
        parse_link = self.__parse_url % (self.__url, barcode)
        # Результат работы
        result_list = []

        # Отбираем данные из таблицы с тегом valign="top"
        data = self.__parse(parse_link)
        # Если данных нет, то делаем еще один запрос
        if len(data) == 0 and len(self.__grab.doc.cookies.get_dict()) == 1:
            self.__authorization()
            data = self.__parse(parse_link)

        if len(data) != 0:
            try:
                # Информация по отправлению
                info = self.__grab.doc.select('//body//p[@class="page_TEXT"]')
                value = info[0].text()
                if len(value) == 0:
                    text = info[1].text().split('[')[0].split(':')[1].strip()
                else:
                    text = info[0].text().split(':')[1].strip()
                self.__info = text
            except IndexError:
                self.__info = ''

            # Перебираем полученные строки таблицы
            for row in data:
                line_list = []
                # пропускаем не нужную ячейку
                if row.text()[0] == '-':
                    continue
                # получаем все ячейки в строке
                data_line = row.select('.//td')

                for cols in data_line:
                    line_list.append(cols.text())
                # удаляем последний пустой элемент
                line_list.pop()
                result_list.append(line_list)
            self.__data = result_list

    # Получает информацию по ШПИ в объект
    def check_num_object(self, barcode):
        self.check_num(barcode)
        return self.data_object

    # Возвращает ШПИ текущего отправления
    @property
    def barcode(self):
        return self.__barcode

    # Возвращает данные по текущему отправлению
    @property
    def info(self):
        return self.__info

    # Возвращает данные по РПО
    @property
    def data(self):
        return self.__data

    # Возвращает данные по РПО в виде списка объектов
    @property
    def data_object(self):
        rpo_info = RpoInfoMail(self.barcode, info=self.__info, raw_data=self.__data)
        rpo_info.parse()
        return rpo_info

    # Возвращает время ожидание соединения
    @property
    def connect_timeout(self):
        return self.__connect_timeout

    # Устанавливает время ожидания соединения
    @connect_timeout.setter
    def connect_timeout(self, value):
        if value:
            try:
                self.__connect_timeout = int(value)
                self.__grab.setup(connect_timeout=self.__connect_timeout, timeout=self.__timeout)
            except ValueError:
                pass

    # Возвращает время ожидания ответа от сервера
    @property
    def timeout(self):
        return self.__timeout

    # Устанавливает время ожидания ответа от сервера
    @timeout.setter
    def timeout(self, value):
        if value:
            try:
                self.__timeout = int(value)
                self.__grab.setup(connect_timeout=self.__connect_timeout, timeout=self.__timeout)
            except ValueError:
                pass


# Объект с информацией об операции над РПО
class RpoInfoOperation:

    # Конструктор
    def __init__(self, num, data_list):
        self._num_cols = len(data_list)
        self._num_line = num
        self._data = data_list

        # Имя операции
        self._oper_name = ''
        # Дата операции
        self._oper_date = ''
        # Индекс места операции
        self._oper_index = ''
        # Название места операции
        self._oper_city = ''
        # Область места операции
        self._oper_area = ''
        # Атрибут операции
        self._oper_attr = ''
        # Вес отправления
        self._mail_mass = ''
        # Объем отправления
        self._mail_size = ''
        # Объявленная ценность отправления
        self._mail_value = ''
        # Наложенный платеж отправления
        self._mail_payment = ''
        # Таможенный сбор отправления
        self._main_custom = ''
        # Индекс адресата
        self._addr_index = ''
        # Город адресата
        self._addr_city = ''
        # Область адресата
        self._addr_area = ''
        # Дата приема файла в ОАСУ
        self._oasu_date_rec = ''
        # Дата загрузки файла в ОАСУ
        self._oasu_date_load = ''
        # Имя программы
        self._soft_name = ''
        # Версия программы
        self._soft_version = ''
        # Парсим данные
        self.parse()

    # Парсит адрес
    def parse_address(self, address):
        city = address.split(',')
        if len(city) > 1:
            return city[0].strip(), city[-1].strip()
        else:
            return city[0].strip(), ''

    # Парсит данные
    def parse(self):
        if len(self._data) == 16:
            self._oper_name = self._data[0]
            self._oper_date = self._data[1]
            self._oper_index = self._data[2]
            self._oper_city, self._oper_area = self.parse_address(self._data[3])
            self._oper_attr = self._data[4]

            try:
                self._mail_mass = int(float(self._data[5]) * 1000)
            except ValueError:
                self._mail_mass = self._data[5]

            self._mail_size = self._data[6]
            self._mail_value = self._data[7]
            self._mail_payment = self._data[8]
            self._main_custom = self._data[9]
            self._addr_index = self._data[10]
            self._addr_city, self._addr_area = self.parse_address(self._data[11])
            self._oasu_date_rec = self._data[12]
            self._oasu_date_load = self._data[13]
            self._soft_name = self._data[14]
            self._soft_version = self._data[15]

    # Системный метод: Размер данных
    def __len__(self):
        return len(self._data)

    # Системный метод: Получить значение элемента
    def __getitem__(self, index):
        if type(index) == int and (index < len(self)):
            return self._data[index]

    # Имя операции
    @property
    def oper_name(self):
        return self._oper_name

    @oper_name.setter
    def oper_name(self, value):
        self._oper_name = value

    # Дата операции
    @property
    def oper_date(self):
        return self._oper_date

    @oper_date.setter
    def oper_date(self, value):
        self._oper_date = value

    # Индекс места операции
    @property
    def oper_index(self):
        return self._oper_index

    @oper_index.setter
    def oper_index(self, value):
        self.oper_index = value

    # Город места операции
    @property
    def oper_city(self):
        return self._oper_city

    @oper_city.setter
    def oper_city(self, value):
        self._oper_city = value

    # Область места операции
    @property
    def oper_area(self):
        return self._oper_area

    @oper_area.setter
    def oper_area(self, value):
        self._oper_area = value

    # Атрибут операции
    @property
    def oper_attr(self):
        return self._oper_attr

    @oper_attr.setter
    def oper_attr(self, value):
        self._oper_attr = value

    # Вес отправления
    @property
    def mail_mass(self):
        return self._mail_mass

    @mail_mass.setter
    def mail_mass(self, value):
        self._mail_mass = value

    # Объем отправления
    @property
    def mail_size(self):
        return self._mail_size

    @mail_size.setter
    def mail_size(self, value):
        self._mail_size = value

    # Объявленная ценность отправления
    @property
    def mail_value(self):
        return self._mail_value

    @mail_value.setter
    def mail_value(self, value):
        self._mail_value = value

    # Наложенный платеж отправления
    @property
    def mail_payment(self):
        return self._mail_payment

    @mail_payment.setter
    def mail_payment(self, value):
        self._mail_payment = value

    # Таможенный сбор отправления
    @property
    def mail_custom(self):
        return self._main_custom

    @mail_custom.setter
    def mail_custom(self, value):
        self._main_custom = value

    # Индекс адресата
    @property
    def address_index(self):
        return self._addr_index

    @address_index.setter
    def address_index(self, value):
        self._addr_index = value

    # Город адресата
    @property
    def address_city(self):
        return self._addr_city

    @address_city.setter
    def address_city(self, value):
        self._addr_city = value

    # Область адресата
    @property
    def address_area(self):
        return self._addr_area

    @address_area.setter
    def address_area(self, value):
        self._addr_area = value

    # Дата приема операции в ОАСУ
    @property
    def oasu_date_rec(self):
        return self._oasu_date_rec

    @oasu_date_rec.setter
    def oasu_date_rec(self, value):
        self._oasu_date_rec = value

    # Дата загрузки операции в ОАСУ
    @property
    def oasu_date_load(self):
        return self._oasu_date_load

    @oasu_date_load.setter
    def oasu_date_load(self, value):
        self._oasu_date_load = value

    # Имя программы
    @property
    def soft_name(self):
        return self._soft_name

    @soft_name.setter
    def soft_name(self, value):
        self._soft_name = value

    # Версия программы
    @property
    def soft_version(self):
        return self._soft_version

    @soft_version.setter
    def soft_version(self, value):
        self._soft_version = value

    # Номер строки
    @property
    def num(self):
        return self._num_line


# Объект отправления
class RpoInfoMail:

    # Конструктор
    def __init__(self, barcode=None, info=None, raw_data=None):

        self._raw_data = []
        self._ind = -1

        if raw_data:
            self._raw_data = raw_data

        self._data = []

        self._info = {'Barcode': '', 'MailType': '', 'MailRank': '', 'PostMark': '',
                      'SendIndex': '', 'SendCity': '', 'SendArea': '',
                      'AddrIndex': '', 'AddrCity': '', 'AddrArea': '',
                      'MailMass': '', 'Value': '', 'Payment': '',
                      'FirstDate': '', 'LastDate': '',
                      'Reception': '', 'Handed': '', 'Arrived': '', 'Return': '',
                      'DaysOfPath': '', 'Delivery': '', 'Left': ''}

        if barcode:
            self._info['Barcode'] = barcode

        if info:
            self.parse_info(info)

    # Парсит данные строк операций
    def parse(self, barcode=None, info=None, raw_data=None, collect_info=True):

        if barcode:
            self._info['Barcode'] = barcode

        if info:
            self.parse_info(info)

        if raw_data:
            data = raw_data
        else:
            data = self._raw_data

        if len(data) <= 0:
            return False

        self._data = []

        for num, line in enumerate(data):
            oper = RpoInfoOperation(num, line)
            oper.parse()

            # Если надо собрать информацию
            if collect_info:
                self.stat(oper)

            if num == 0:
                self._info['FirstDate'] = oper.oper_date

            if num == len(data) - 1:
                self._info['LastDate'] = oper.oper_date

            self._data.append(oper)

        self._info['DaysOfPath'] = self.days_of_path()
        return True

    # Парсит информацию по отправлению
    def parse_info(self, info):
        data = info.split(',')
        if len(data) > 2:
            self._info['MailType'] = data[0].strip()
            self._info['MailRank'] = data[1].strip()
            self._info['PostMark'] = data[2].strip()

    # Возвращает количество дней в пути
    def days_of_path(self):
        if self._info['LastDate'] and self._info['FirstDate']:
            try:
                first = datetime.strptime(self._info['FirstDate'], '%d.%m.%Y %H:%M:%S')
            except ValueError:
                try:
                    first = datetime.strptime(self._info['FirstDate'], '%d.%m.%Y')
                except ValueError:
                    first = datetime.now()

            try:
                last = datetime.strptime(self._info['LastDate'], '%d.%m.%Y %H:%M:%S')
            except ValueError:
                try:
                    last = datetime.strptime(self._info['LastDate'], '%d.%m.%Y')
                except ValueError:
                    last = datetime.now()

            range_date = last - first
            hour = range_date.seconds // (60 * 60)

            if hour:
                return '%sд %sч' % (range_date.days, hour)
            else:
                return '%sд' % range_date.days
        return ''

    # Ведет статистику
    def stat(self, oper):
        if oper.oper_name == 'Приём':
            self._info['Reception'] = oper.oper_date
            self._info['SendIndex'] = oper.oper_index
            self._info['SendCity'] = oper.oper_city
            self._info['SendArea'] = oper.oper_area

        if oper.oper_name == 'Обработка' and oper.oper_attr == 'Прибыло в место вручения':
            self._info['Arrived'] = oper.oper_date

        if oper.oper_name == 'Доставка' and oper.oper_attr == 'Доставлено в почтовый ящик':
            self._info['Delivery'] = oper.oper_date

        if oper.oper_name == 'Обработка' and oper.oper_attr == 'Покинуло место приёма' \
                and oper.oper_index == self._info['AddrIndex']:
            self._info['Left'] = oper.oper_date

        if oper.oper_name == 'Возврат':
            self._info['Return'] = oper.oper_date

        if oper.oper_name == 'Вручение':
            self._info['Handed'] = oper.oper_date

            if not self._info['AddrIndex'] and oper.oper_index:
                self._info['AddrIndex'] = oper.oper_index

            if not self._info['AddrCity'] and oper.oper_city:
                self._info['AddrCity'] = oper.oper_city

            if not self._info['AddrArea'] and oper.oper_area:
                self._info['AddrArea'] = oper.oper_area

        if oper.address_index and not self._info['AddrIndex']:
            self._info['AddrIndex'] = oper.address_index

        if oper.address_city and not self._info['AddrCity']:
            self._info['AddrCity'] = oper.address_city

        if oper.address_area and not self._info['AddrArea']:
            self._info['AddrArea'] = oper.address_area

        if oper.mail_mass and not self._info['MailMass']:
            self._info['MailMass'] = oper.mail_mass

        if oper.mail_value and not self._info['Value']:
            self._info['Value'] = oper.mail_value

        if oper.mail_payment and not self._info['Payment']:
            self._info['Payment'] = oper.mail_payment

    # Системный метод: Размер данных
    def __len__(self):
        return len(self._data)

    # Системный метод: Данные в строку
    def __str__(self):
        return '{ ШПИ: %s, ОПС: %s, Дата: %s, Куда: %s, Вес: %s, Вид: %s}' \
               % (self._info['Barcode'], self._info['SendIndex'], self._info['FirstDate'], self._info['AddrIndex'],
                  self._info['MailMass'], self._info['MailType'])

    # Системный метод: Вывод на консоль
    def __repr__(self):
        return str(self)

    # Системный метод: Итератор
    def __iter__(self):
        return self

    # Системный метод: Возвращает следующий элемент
    def __next__(self):
        if self._ind == len(self) - 1:
            self._ind = -1
            raise StopIteration
        self._ind += 1
        return self._data[self._ind]

    # Системный метод: Получить значение элемента
    def __getitem__(self, index):
        if type(index) == int and (index < len(self)):
            return self._data[index]

    @property
    def data(self):
        return self._data

    @property
    def info(self):
        return self._info
