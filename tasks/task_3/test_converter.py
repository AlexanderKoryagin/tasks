#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pytest


class Locators(object):

    locator_filter_block_css = 'div.rates-aside-filter.rates-container'
    locator_widgets_class = 'widget-rates'
    locator_convert_block_css = 'div.filter-block.filter-block-converter'
    locator_num_input_xpath = u"//input[@placeholder='Сумма']"

    locator_show_button_xpath = u"//button[contains(text(),'Показать')]"
    locator_results_css = 'div.converter-result'

    locator_currency_selector_block_class = 'select'
    locator_currency_dropdown_css = "div[class='select opened']"
    locator_currency_in_dropdown_xpath = (
        "//div[@class='visible']/span[contains(text(), '{currency}')]")

    locator_source_block_xpath = (
        "//div[@class='filter-block' and @data-reactid='.s.$1.$0.1']")
    locator_source_block_radio_sber_card_xpath = (
        "//span[@class='radio' and @data-reactid='.s.$1.$0.1.1:$0.1']")
    locator_source_block_radio_bank_account_xpath = (
        "//span[@class='radio' and @data-reactid='.s.$1.$0.1.1:$1.1']")
    locator_source_block_radio_cash_xpath = (
        "//span[@class='radio' and @data-reactid='.s.$1.$0.1.1:$2.1']")

    Locator_receipt_block_xpath = (
        "//div[@class='filter-block' and @data-reactid='.s.$1.$0.2']")
    locator_receipt_block_radio_to_card_xpath = (
        "//span[@class='radio' and @data-reactid='.s.$1.$0.2.1:$0.1']")
    locator_receipt_block_radio_to_bank_account_xpath = (
        "//span[@class='radio' and @data-reactid='.s.$1.$0.2.1:$1.1']")
    locator_receipt_block_radio_cash_xpath = (
        "//span[@class='radio' and @data-reactid='.s.$1.$0.2.1:$2.1']")

    locator_exchange_method_block_xpath = (
        "//div[@class='filter-block' and @data-reactid='.s.$1.$0.3']")
    locator_exchange_method_block_radio_internet_bank_xpath = (
        "//span[@class='radio' and @data-reactid='.s.$1.$0.3.1:$0.1']")
    locator_exchange_method_block_radio_bank_office_xpath = (
        "//span[@class='radio' and @data-reactid='.s.$1.$0.3.1:$1.1']")
    locator_exchange_method_block_radio_atm_xpath = (
        "//span[@class='radio' and @data-reactid='.s.$1.$0.3.1:$2.1']")

    locator_time_block_xpath = (
        "//div[@class='filter-block' and @data-reactid='.s.$1.$0.5']")
    locator_time_block_radio_now_xpath = (
        "//span[@class='radio' and @data-reactid='.s.$1.$0.5.1:$0.1']")
    locator_time_block_radio_choose_xpath = (
        "//span[@class='radio' and @data-reactid='.s.$1.$0.5.1:$1.1']")
    locator_time_block_datepicker_css = (
        "div[class='filter-datepicker input']")


class ConverterPage(Locators):

    driver = webdriver.Firefox()

    converter_url = 'http://www.sberbank.ru/ru/quotes/converter'
    # not all variants, just basic
    currency_list = ['RUR', 'USD', 'CAD', 'EUR', 'JPY', 'CHF', 'AUD', 'GBP']
    timeout = 15  # seconds

    def open_page(self):
        """Open page in browser and wait till it'll be loaded."""
        self.driver.get(self.converter_url)
        wait = WebDriverWait(self.driver, self.timeout)
        wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME,
                                              self.locator_widgets_class)))

    def _filter_block(self):
        """Find filter block from page.
        :return: selenium object
        """
        filter_block = self.driver.find_element_by_css_selector(
            self.locator_filter_block_css)
        return filter_block

    def _convert_block(self):
        """Find block with converter from page.
        :return: selenium object
        """
        filter_block = self._filter_block()
        convert_block = filter_block.find_element_by_css_selector(
            self.locator_convert_block_css)
        return convert_block

    def source_block(self):
        """Find block with source selector and it's buttons on page.
        :return: dict with selenium objects
        """
        filter_block = self._filter_block()

        source_block = filter_block.find_element_by_xpath(
            self.locator_source_block_xpath)

        radio_sber_card = source_block.find_element_by_xpath(
            self.locator_source_block_radio_sber_card_xpath)
        radio_bank_account = source_block.find_element_by_xpath(
            self.locator_source_block_radio_bank_account_xpath)
        radio_cash = source_block.find_element_by_xpath(
            self.locator_source_block_radio_cash_xpath)

        return {'radio_sber_card': radio_sber_card,
                'radio_bank_account': radio_bank_account,
                'radio_cash': radio_cash,
                'source_block': source_block}

    def receipt_block(self):
        """Find block with receipt selector and it's buttons on page.
        :return: dict with selenium objects
        """
        filter_block = self._filter_block()

        receipt_block = filter_block.find_element_by_xpath(
            self.Locator_receipt_block_xpath)

        radio_to_card = receipt_block.find_element_by_xpath(
            self.locator_receipt_block_radio_to_card_xpath)
        radio_to_bank_account = receipt_block.find_element_by_xpath(
            self.locator_receipt_block_radio_to_bank_account_xpath)
        radio_cash = receipt_block.find_element_by_xpath(
            self.locator_receipt_block_radio_cash_xpath)

        return {'radio_to_card': radio_to_card,
                'radio_to_bank_account': radio_to_bank_account,
                'radio_cash': radio_cash,
                'receipt_block': receipt_block}

    def exchange_method_block(self):
        """Find block with exchange method selector and it's buttons on page.
        :return: dict with selenium objects
        """
        filter_block = self._filter_block()

        exchange_method_block = filter_block.find_element_by_xpath(
            self.locator_exchange_method_block_xpath)

        radio_internet_bank = exchange_method_block.find_element_by_xpath(
            self.locator_exchange_method_block_radio_internet_bank_xpath)
        radio_bank_office = exchange_method_block.find_element_by_xpath(
            self.locator_exchange_method_block_radio_bank_office_xpath)
        radio_atm = exchange_method_block.find_element_by_xpath(
            self.locator_exchange_method_block_radio_atm_xpath)

        return {'radio_internet_bank': radio_internet_bank,
                'radio_bank_office': radio_bank_office,
                'radio_atm': radio_atm,
                'exchange_method_block': exchange_method_block}

    def time_block(self):
        """Find block with time selector and it's buttons on page.
        :return: dict with selenium objects
        """
        filter_block = self._filter_block()

        time_block = filter_block.find_element_by_xpath(
            self.locator_time_block_xpath)

        radio_now = time_block.find_element_by_xpath(
            self.locator_time_block_radio_now_xpath)
        radio_choose = time_block.find_element_by_xpath(
            self.locator_time_block_radio_choose_xpath)

        return {'radio_now': radio_now,
                'radio_choose': radio_choose,
                'time_block': time_block}

    def set_num_to_convert(self, num_to_convert):
        """Set amount of money you want to convert.
        :param num_to_convert: int
        """
        if not isinstance(num_to_convert, int):
            raise ValueError("Value for conversion should be int")

        convert_block = self._convert_block()

        num_input_form = convert_block.find_element_by_xpath(
            self.locator_num_input_xpath)
        num_input_form.clear()
        num_input_form.send_keys(num_to_convert)

    def set_currency_from_to(self, from_currency, to_currency):
        """Set currency conversion: FROM and TO.
        :param from_currency: short name of currency
        :param to_currency: short name of currency
        """
        from_currency = str(from_currency).upper()
        to_currency = str(to_currency).upper()

        assert (from_currency in self.currency_list and
                to_currency in self.currency_list), (
                    "Provided currency [{0} -> {1}] is not in a list of "
                    "available variants: {2}".format(
                        from_currency, to_currency, self.currency_list))

        convert_block = self._convert_block()

        currency_selector_blocks = convert_block.find_elements_by_class_name(
            self.locator_currency_selector_block_class)
        from_currency_block = currency_selector_blocks[0]
        to_currency_block = currency_selector_blocks[1]

        # FROM
        from_currency_block.click()
        from_currency_dropdown = convert_block.find_element_by_css_selector(
            self.locator_currency_dropdown_css)

        from_currency_in_dropdown = (
            from_currency_dropdown.find_element_by_xpath(
                self.locator_currency_in_dropdown_xpath.format(
                    currency=from_currency)))
        from_currency_in_dropdown.location_once_scrolled_into_view
        from_currency_in_dropdown.click()

        # TO
        to_currency_block.click()
        to_currency_dropdown = convert_block.find_element_by_css_selector(
            self.locator_currency_dropdown_css)

        to_currency_in_dropdown = (
            to_currency_dropdown.find_element_by_xpath(
                self.locator_currency_in_dropdown_xpath.format(
                    currency=to_currency)))

        to_currency_in_dropdown.location_once_scrolled_into_view
        to_currency_in_dropdown.click()

    def click_apply_button(self):
        """Find and click on Show button"""
        filter_block = self._filter_block()
        show_button = filter_block.find_element_by_xpath(
            self.locator_show_button_xpath)
        show_button.click()

    def get_results(self):
        """Wait and find results of conversation.
        :return: text from results.
        """
        wait = WebDriverWait(self.driver, self.timeout)
        result_form = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                                              self.locator_results_css)))
        return result_form.text


class TestConverter(ConverterPage):

    @pytest.yield_fixture(scope='session', autouse=True)
    def prepare(self):
        # open converter page
        self.open_page()
        yield
        # close converter page
        self.driver.close()

    def read_csv(self):
        """Read CSV file and convert it parameters for test.
        :return: list
        """
        params = []
        csv_file = 'params.csv'
        csv_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            csv_file)
        with open(csv_file_path, 'r') as csv_f:
            reader = csv.DictReader(csv_f, delimiter=',', quotechar="'")
            for row in reader:
                params.append([int(row['Money to convert']),
                               row['Currency from'],
                               row['Currency to']])
        return params

    def test_converter_different_currencies(self):
        """Test different currencies in converter.

        Actions:
        1. Read 'Money to convert', 'Currency from', 'Currency to' from CSV.
        2. Set value in converter.
        3. Set FROM and TO currency.
        4. Click apply button.
        5. Get results.
        6. Check content of results.
        """
        # get params from csv file
        for param in self.read_csv():
            money, curr_from, curr_to = param

            step_name = 'Set value in converter: {0}'.format(money)
            with pytest.allure.step(step_name):
                self.set_num_to_convert(money)

            step_name = 'Set FROM [{0}] and TO [{1}]currency'.format(
                curr_from, curr_to)
            with pytest.allure.step(step_name):
                self.set_currency_from_to(curr_from, curr_to)

            with pytest.allure.step('Click apply button'):
                self.click_apply_button()

            with pytest.allure.step('Get results'):
                results = self.get_results()

            with pytest.allure.step('Check content of results'):
                results = ''.join(results.splitlines())
                results = results.replace(" ", "")
                print results

                assert str(money) in results
                assert all(i in results for i in (curr_from, curr_to)), (
                    'Currency not in results: {0} -> {1}\n'
                    'results: {2}'.format(
                        curr_from, curr_to, results.encode('utf-8')))

    def test_inactive_radiobuttons_in_exchange_method_block(self):
        """Test that with some configuration some checkboxes became inactive.

        Actions:
        1. Enable 'cash' checkbox from 'source' block.
        2. Enable 'cash' checkbox from 'receipt' block.
        3. Check that in 'exchange method' block two radio-buttons are not
        enabled.
        """
        not_active_boxes = (u'Интернет-банк', u'Банкомат / УС')

        source_block = self.source_block()
        receipt_block = self.receipt_block()

        with pytest.allure.step("Enable 'cash' checkbox from 'source' block"):
            source_block['radio_cash'].click()

        with pytest.allure.step("Enable 'cash' checkbox from 'receipt' block"):
            receipt_block['radio_cash'].click()

        with pytest.allure.step("Get 'exchange method' block"):
            exchange_method_block = self.exchange_method_block()
            exchange_method_block = exchange_method_block[
                'exchange_method_block']

            inactve_elements = (exchange_method_block.
                                find_elements_by_class_name('filter-inactive'))

            inactve_elements_names = [x.text.strip() for x in inactve_elements]

        with pytest.allure.step("Check that some elemens are not anabled"):
            assert all(i in inactve_elements_names
                       for i in not_active_boxes), (
                           "Some of the checkboxes are enabled")

    def test_calendar_appears(self):
        """Test that date-picker calendar appears if 'select' time pressed.

        Actions:
        1. In time block select current time.
        2. Check that Date-picker is not present.
        3. In time box select 'choose' time.
        4. Check that Date-picker presents.
        """
        with pytest.allure.step("In time block select current time"):
            self.time_block()['radio_now'].click()

        with pytest.allure.step("Check that Date-picker is not present"):
            assert not (self.time_block()['time_block'].
                        find_elements_by_css_selector(
                            self.locator_time_block_datepicker_css)), (
                                "Date-picker present, but it should not")

        with pytest.allure.step("In time box select 'choose' time"):
            self.time_block()['radio_choose'].click()

        with pytest.allure.step("Check that Date-picker presents"):
            assert (len(self.time_block()['time_block'].
                        find_elements_by_css_selector(
                            self.locator_time_block_datepicker_css)) == 1), (
                                "Date-picker does not present, but it should")
