#!/usr/bin/env python
# -*- coding: utf-8 -*-


from grab import Grab
from grab.error import (GrabTimeoutError, GrabAuthError)
from .errors import *
from datetime import datetime


__author__ = 'WorldCount'


# Объект с информацией об операции над РПО
class RpoInfoOperation:

    # Конструктор
    def __init__(self, num, data_list):
        """
        :param num: Номер строки
        :param data_list: Данные строки
        """

        # Количество столбцов с данными
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
        """
        :param address: Строка с адресом
        :return: Массив с распарсенными данными
        """
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
        """
        :param barcode: Штрих-код отправления
        :param info: Информация об отправлении
        :param raw_data: Сырые данные об отправлении
        """

        self._raw_data = []
        self._ind = -1

        if raw_data:
            self._raw_data = raw_data

        self._data = []

        self._infoEn = {'Barcode': '', 'MailType': '', 'MailRank': '', 'PostMark': '',
                        # Отправитель
                        'SendIndex': '', 'SendCity': '', 'SendArea': '',
                        # Получатель
                        'AddrIndex': '', 'AddrCity': '', 'AddrArea': '',
                        'MailMass': '', 'Value': '', 'Payment': '',
                        # Дата первой операции, дата последней операции, дней в пути
                        'FirstOperDate': '', 'LastOperDate': '',
                        'DaysOfPath': '', 'HoursOfPath': '', 'FullTimeIfPath': '',

                        # Прием
                        'ReceptionDate': '', 'ReceptionSoft': '', 'ReceptionVersion': '', 'ReceptionIndex': '',
                        # Прибыло
                        'ArrivedDate': '', 'ArrivedSoft': '', 'ArrivedVersion': '', 'ArrivedIndex': '',
                        # Вручение
                        'HandedDate': '', 'HandedSoft': '', 'HandedVersion': '', 'HandedIndex': '',
                        # Доставка
                        'DeliveryDate': '', 'DeliverySoft': '', 'DeliveryVersion': '', 'DeliveryIndex': '',
                        # Возврат
                        'ReturnDate': '', 'ReturnSoft': '', 'ReturnVersion': '', 'ReturnIndex': '', 'ReturnToIndex': '',
                        # Покинуло место приема
                        'SendLeftDate': '', 'SendLeftSoft': '', 'SendLeftVersion': '', 'SendLeftIndex': '',
                        # Покинуло место возврата
                        'ReturnLeftDate': '', 'ReturnLeftSoft': '', 'ReturnLeftVersion': '', 'ReturnLeftIndex': '',
                        # Досыл
                        'SentDate': '', 'SentSoft': '', 'SentVersion': '', 'SentIndex': '', 'SentToIndex': '',

                        # Последняя операция
                        'LastOperName': '', 'LastOperAttr': '', 'LastOperIndex': '',  'LastOperCity': ''}

        self._infoRu = {'ШПИ': '', 'Вид': '', 'Разряд': '', 'Отметки': '',
                        'ИндексОтправителя': '', 'ГородОтправителя': '', 'ОбластьОтправителя': '',
                        'ИндексПолучателя': '', 'ГородПолучателя': '', 'ОбластьПолучателя': '',
                        'Вес': '', 'Ценность': '', 'Платеж': '',
                        'ПерваяОперацияДата': '', 'ПоследняяОперацияДата': '', 'ДнейВПути': '', 'ЧасовВПути': '',
                        'ВремяВПути': '',

                        'ПриемДата': '', 'ПриемСофт': '', 'ПриемВерсия': '', 'ПриемИндекс': '',
                        'ПрибылоДата': '', 'ПрибылоСофт': '', 'ПрибылоВерсия': '', 'ПрибылоИндекс': '',
                        'ВручениеДата': '', 'ВручениеСофт': '', 'ВручениеВерсия': '', 'ВручениеИндекс': '',
                        'ДоставкаДата': '', 'ДоставкаСофт': '', 'ДоставкаВерсия': '', 'ДоставкаИндекс': '',
                        'ВозвратДата': '', 'ВозвратСофт': '', 'ВозвратВерсия': '', 'ВозвратИндекс': '',
                        'ВозвратКудаИндекс': '',
                        'ПокинулоПриемДата': '', 'ПокинулоПриемСофт': '', 'ПокинулоПриемВерсия': '',
                        'ПокинулоПриемИндекс': '',
                        'ПокинулоВозвратДата': '', 'ПокинулоВозвратСофт': '', 'ПокинулоВозвратВерсия': '',
                        'ПокинулоВозвратИндекс': '',
                        'ДосылДата': '', 'ДосылСофт': '', 'ДосылВерсия': '', 'ДосылИндекс': '', 'ДосылКудаИндекс': '',
                        # Последняя операция
                        'ПоследняяОперацияНазвание': '', 'ПоследняяОперацияАтрибут': '',
                        'ПоследняяОперацияИндекс': '', 'ПоследняяОперацияМесто': ''
                        }

        if barcode:
            self._infoEn['Barcode'] = barcode
            self._infoRu['ШПИ'] = barcode

        if info:
            self.parse_info(info)

    # Парсит данные строк операций
    def parse(self, barcode=None, info=None, raw_data=None, collect_info=True):
        """
        :param barcode: Штрих-код отправления
        :param info: Информация об отправлении
        :param raw_data: Сырые данные об отправлении
        :param collect_info: Собирать информацию
        :return: Парсинг прошел успешно
        """

        if barcode:
            self._infoEn['Barcode'] = barcode
            self._infoRu['ШПИ'] = barcode

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
                self._infoEn['FirstOperDate'] = oper.oper_date
                self._infoRu['ПерваяОперацияДата'] = self._infoEn['FirstOperDate']

            if num == len(data) - 1:
                # EN
                self._infoEn['LastOperName'] = oper.oper_name
                self._infoEn['LastOperAttr'] = oper.oper_attr
                self._infoEn['LastOperDate'] = oper.oper_date
                self._infoEn['LastOperIndex'] = oper.oper_index
                self._infoEn['LastOperCity'] = oper.oper_city
                # RU
                self._infoRu['ПоследняяОперацияНазвание'] = self._infoEn['LastOperName']
                self._infoRu['ПоследняяОперацияАтрибут'] = self._infoEn['LastOperAttr']
                self._infoRu['ПоследняяОперацияДата'] = self._infoEn['LastOperDate']
                self._infoRu['ПоследняяОперацияИндекс'] = self._infoEn['LastOperIndex']
                self._infoRu['ПоследняяОперацияМесто'] = self._infoEn['LastOperCity']

            self._data.append(oper)

        days, hours = self.days_of_path()
        # EN
        if hours:
            self._infoEn['FullTimeIfPath'] = '{0}д {1}ч'.format(days, hours)
        else:
            self._infoEn['FullTimeIfPath'] = '{0}д'.format(days)
        self._infoEn['DaysOfPath'] = days
        self._infoEn['HoursOfPath'] = hours
        # RU
        self._infoRu['ВремяВПути'] = self._infoEn['FullTimeIfPath']
        self._infoRu['ДнейВПути'] = self._infoEn['DaysOfPath']
        self._infoRu['ЧасовВПути'] = self._infoEn['HoursOfPath']
        return True

    # Парсит информацию по отправлению
    def parse_info(self, info):
        """
        :param info: Строка с информацией
        :return: Парсинг прошел успешно
        """
        data = info.split(',')
        if len(data) > 2:
            # EN
            self._infoEn['MailType'] = data[0].strip()
            self._infoEn['MailRank'] = data[1].strip()
            self._infoEn['PostMark'] = data[2].strip()
            # RU
            self._infoRu['Вид'] = self._infoEn['MailType']
            self._infoRu['Разряд'] = self._infoEn['MailRank']
            self._infoRu['Отметки'] = self._infoEn['PostMark']
            return True
        return False

    # Возвращает количество дней в пути
    def days_of_path(self):
        if self._infoEn['LastOperDate'] and self._infoEn['FirstOperDate']:
            try:
                first = datetime.strptime(self._infoEn['FirstOperDate'], '%d.%m.%Y %H:%M:%S')
            except ValueError:
                try:
                    first = datetime.strptime(self._infoEn['FirstOperDate'], '%d.%m.%Y')
                except ValueError:
                    first = datetime.now()

            try:
                last = datetime.strptime(self._infoEn['LastOperDate'], '%d.%m.%Y %H:%M:%S')
            except ValueError:
                try:
                    last = datetime.strptime(self._infoEn['LastOperDate'], '%d.%m.%Y')
                except ValueError:
                    last = datetime.now()

            range_date = last - first
            hour = range_date.seconds // (60 * 60)
            return range_date.days, hour
        return 0, 0

    # Ведет статистику
    def stat(self, oper):
        # ПРИЕМ
        if oper.oper_name == 'Приём':
            # EN
            self._infoEn['ReceptionDate'] = oper.oper_date
            self._infoEn['ReceptionSoft'] = oper.soft_name
            self._infoEn['ReceptionVersion'] = oper.soft_version
            self._infoEn['ReceptionIndex'] = oper.oper_index
            self._infoEn['SendIndex'] = oper.oper_index
            self._infoEn['SendCity'] = oper.oper_city
            self._infoEn['SendArea'] = oper.oper_area
            # RU
            self._infoRu['ПриемДата'] = self._infoEn['ReceptionDate']
            self._infoRu['ПриемСофт'] = self._infoEn['ReceptionSoft']
            self._infoRu['ПриемВерсия'] = self._infoEn['ReceptionVersion']
            self._infoRu['ПриемИндекс'] = self._infoEn['ReceptionIndex']
            self._infoRu['ИндексОтправителя'] = self._infoEn['SendIndex']
            self._infoRu['ГородОтправителя'] = self._infoEn['SendCity']
            self._infoRu['ОбластьОтправителя'] = self._infoEn['SendArea']

        # ПРИБЫЛО
        if oper.oper_name == 'Обработка' and oper.oper_attr == 'Прибыло в место вручения':
            # EN
            self._infoEn['ArrivedDate'] = oper.oper_date
            self._infoEn['ArrivedSoft'] = oper.soft_name
            self._infoEn['ArrivedVersion'] = oper.soft_version
            self._infoEn['ArrivedIndex'] = oper.oper_index
            # RU
            self._infoRu['ПрибылоДата'] = self._infoEn['ArrivedDate']
            self._infoRu['ПрибылоВерсия'] = self._infoEn['ArrivedSoft']
            self._infoRu['ПрибылоСофт'] = self._infoEn['ArrivedVersion']
            self._infoRu['ПрибылоИндекс'] = self._infoEn['ArrivedIndex']

        # ДОСЫЛ
        if oper.oper_name == 'Досылка почты':
            # EN
            self._infoEn['SentDate'] = oper.oper_date
            self._infoEn['SentSoft'] = oper.soft_name
            self._infoEn['SentVersion'] = oper.soft_version
            self._infoEn['SentIndex'] = oper.oper_index
            self._infoEn['SentToIndex'] = oper.address_index
            # RU
            self._infoRu['ДосылДата'] = self._infoEn['SentDate']
            self._infoRu['ДосылСофт'] = self._infoEn['SentSoft']
            self._infoRu['ДосылВерсия'] = self._infoEn['SentVersion']
            self._infoRu['ДосылИндекс'] = self._infoEn['SentIndex']
            self._infoRu['ДосылКудаИндекс'] = self._infoEn['SentToIndex']

        # ПОКИНУЛО
        if oper.oper_name == 'Обработка':
            if oper.oper_attr == 'Покинуло место приёма' or oper.oper_attr == 'Покинуло сортировочный центр':
                # Покинуло прием
                if oper.oper_index == self._infoEn['SendIndex']:
                    # EN
                    self._infoEn['SendLeftDate'] = oper.oper_date
                    self._infoEn['SendLeftSoft'] = oper.soft_name
                    self._infoEn['SendLeftVersion'] = oper.soft_version
                    self._infoEn['SendLeftIndex'] = oper.oper_index
                    # RU
                    self._infoRu['ПокинулоПриемДата'] = self._infoEn['SendLeftDate']
                    self._infoRu['ПокинулоПриемСофт'] = self._infoEn['SendLeftSoft']
                    self._infoRu['ПокинулоПриемВерсия'] = self._infoEn['SendLeftVersion']
                    self._infoRu['ПокинулоПриемИндекс'] = self._infoEn['SendLeftIndex']
                # Покинуло возврат
                if oper.oper_index == self._infoEn['AddrIndex']:
                    # EN
                    self._infoEn['ReturnLeftDate'] = oper.oper_date
                    self._infoEn['ReturnLeftSoft'] = oper.soft_name
                    self._infoEn['ReturnLeftVersion'] = oper.soft_version
                    self._infoEn['ReturnLeftIndex'] = oper.oper_index
                    # RU
                    self._infoRu['ПокинулоВозвратДата'] = self._infoEn['ReturnLeftDate']
                    self._infoRu['ПокинулоВозвратСофт'] = self._infoEn['ReturnLeftSoft']
                    self._infoRu['ПокинулоВозвратВерсия'] = self._infoEn['ReturnLeftVersion']
                    self._infoRu['ПокинулоВозвратИндекс'] = self._infoEn['ReturnLeftIndex']

        # ВОЗВРАТ
        if oper.oper_name == 'Возврат':
            # EN
            self._infoEn['ReturnDate'] = oper.oper_date
            self._infoEn['ReturnSoft'] = oper.soft_name
            self._infoEn['ReturnVersion'] = oper.soft_version
            self._infoEn['ReturnIndex'] = oper.oper_index
            self._infoEn['ReturnToIndex'] = oper.address_index
            # RU
            self._infoRu['ВозвратДата'] = self._infoEn['ReturnDate']
            self._infoRu['ВозвратСофт'] = self._infoEn['ReturnSoft']
            self._infoRu['ВозвратВерсия'] = self._infoEn['ReturnVersion']
            self._infoRu['ВозвратИндекс'] = self._infoEn['ReturnIndex']
            self._infoRu['ВозвратКудаИндекс'] = self._infoEn['ReturnToIndex']

        if oper.oper_name == 'Вручение' or \
                (oper.oper_name == 'Доставка' and oper.oper_attr == 'Доставлено в почтовый ящик'):
            # ВРУЧЕНИЕ
            if oper.oper_name == 'Вручение':
                # EN
                self._infoEn['HandedDate'] = oper.oper_date
                self._infoEn['HandedSoft'] = oper.soft_name
                self._infoEn['HandedVersion'] = oper.soft_version
                self._infoEn['HandedIndex'] = oper.oper_index
                # RU
                self._infoRu['ВручениеДата'] = self._infoEn['HandedDate']
                self._infoRu['ВручениеСофт'] = self._infoEn['HandedSoft']
                self._infoRu['ВручениеВерсия'] = self._infoEn['HandedVersion']
                self._infoRu['ВручениеИндекс'] = self._infoEn['HandedIndex']

            # ДОСТАВКА
            if oper.oper_name == 'Доставка':
                # EN
                self._infoEn['DeliveryDate'] = oper.oper_date
                self._infoEn['DeliverySoft'] = oper.soft_name
                self._infoEn['DeliveryVersion'] = oper.soft_version
                self._infoEn['DeliveryIndex'] = oper.oper_index
                # RU
                self._infoRu['ДоставкаДата'] = self._infoEn['DeliveryDate']
                self._infoRu['ДоставкаСофт'] = self._infoEn['DeliverySoft']
                self._infoRu['ДоставкаВерсия'] = self._infoEn['DeliveryVersion']
                self._infoRu['ДоставкаИндекс'] = self._infoEn['DeliveryIndex']

            if not self._infoEn['AddrIndex'] and oper.oper_index:
                self._infoEn['AddrIndex'] = oper.oper_index
                self._infoRu['ИндексПолучателя'] = self._infoEn['AddrIndex']

            if not self._infoEn['AddrCity'] and oper.oper_city:
                self._infoEn['AddrCity'] = oper.oper_city
                self._infoRu['ГородПолучателя'] = self._infoEn['AddrCity']

            if not self._infoEn['AddrArea'] and oper.oper_area:
                self._infoEn['AddrArea'] = oper.oper_area
                self._infoRu['ОбластьПолучателя'] = self._infoEn['AddrArea']

        if oper.address_index and not self._infoEn['AddrIndex']:
            self._infoEn['AddrIndex'] = oper.address_index
            self._infoRu['ИндексПолучателя'] = self._infoEn['AddrIndex']

        if oper.address_city and not self._infoEn['AddrCity']:
            self._infoEn['AddrCity'] = oper.address_city
            self._infoRu['ГородПолучателя'] = self._infoEn['AddrCity']

        if oper.address_area and not self._infoEn['AddrArea']:
            self._infoEn['AddrArea'] = oper.address_area
            self._infoRu['ОбластьПолучателя'] = self._infoEn['AddrArea']

        if oper.mail_mass and not self._infoEn['MailMass']:
            self._infoEn['MailMass'] = oper.mail_mass
            self._infoRu['Вес'] = self._infoEn['MailMass']

        if oper.mail_value and not self._infoEn['Value']:
            self._infoEn['Value'] = oper.mail_value
            self._infoRu['Ценность'] = self._infoEn['Value']

        if oper.mail_payment and not self._infoEn['Payment']:
            self._infoEn['Payment'] = oper.mail_payment
            self._infoRu['Платеж'] = self._infoEn['Payment']

    # Системный метод: Размер данных
    def __len__(self):
        return len(self._data)

    # Системный метод: Данные в строку
    def __str__(self):
        return '{ ШПИ: %s, ОПС: %s, Дата: %s, Куда: %s, Вес: %s, Вид: %s}' \
               % (self._infoEn['Barcode'], self._infoEn['SendIndex'], self._infoEn['FirstDate'],
                  self._infoEn['AddrIndex'], self._infoEn['MailMass'], self._infoEn['MailType'])

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
    def info_en(self):
        return self._infoEn

    @property
    def info_ru(self):
        return self._infoRu


# Получает данные в ОАСУ по ШПИ
class RpoInfo:

    def __init__(self, url='http://vinfo.russianpost.ru', login='post', password='stat', auth=True):
        # Логин и пароль
        self.__login = login
        self.__password = password
        # Настройки соединения
        self.__connect_timeout = 5
        self.__timeout = 5
        # Ссылки
        self.__url = url
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
        result = {'info': '', 'barcode': barcode, 'data': []}
        # Ищем в ОАСУ
        parse_link = self.__parse_url % (self.__url, barcode)
        # Результат работы
        result_list = []

        # Отбираем данные из таблицы с тегом valign="top"
        data = self.__parse(parse_link)
        # Если данных нет, то авторизируемся и делаем еще один запрос
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
                result['info'] = text
            except IndexError:
                result['info'] = ''

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
            result['data'] = result_list
        return result

    # Получает информацию по ШПИ в объект
    def check_num_object(self, barcode):
        info = self.check_num(barcode)
        rpo_info = RpoInfoMail(info['barcode'], info=info['info'], raw_data=info['data'])
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
