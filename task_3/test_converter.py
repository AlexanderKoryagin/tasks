#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pytest


class ConverterPage(object):

    driver = webdriver.Firefox()

    converter_url = 'http://www.sberbank.ru/ru/quotes/converter'
    currency_list = ['RUR', 'USD', 'CAD', 'EUR', 'JPY', 'CHF', 'AUD', 'GBP']
    timeout = 15  # seconds

    locator_filter_block_css = 'div.rates-aside-filter.rates-container'
    locator_widgets_class = 'widget-rates'
    locator_convert_block_css = 'div.filter-block.filter-block-converter'
    locator_num_input_xpath = u"//input[@placeholder='Сумма']"
    locator_currency_selector_block_class = 'select'
    locator_currency_dropdown_css = "div[class='select opened']"
    locator_currency_in_dropdown_xpath = (
        "//div[@class='visible']/span[contains(text(), '{currency}')]")
    locator_show_button_xpath = u"//button[contains(text(),'Показать')]"
    locator_results_css = 'div.converter-result'

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
            "Provided currency [{0} -> {1}] is not in a list of available "
            "variants: {2}".format(
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

    def test_1(self):
        """
        Actions:
        1. Read 'Money to convert', 'Currency from', 'Currency to' from CSV.
        2. Set value in converter.
        3. Set FROM and TO currency.
        4. Click apply button.
        5. Get results.
        6. Check content of results.
        """
        for param in self.read_csv():
            money, curr_from, curr_to = param

            with pytest.allure.step(
                    'Set value in converter: {0}'.format(money)):
                self.set_num_to_convert(money)

            with pytest.allure.step(
                    'Set FROM [{0}] and TO [{1}]currency'.format(
                        curr_from, curr_to)):
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
                    'results: {2}'.format(curr_from, curr_to,
                                          results.encode('utf-8')))
