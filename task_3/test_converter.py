#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pytest


class ConverterPage(object):

    driver = webdriver.Firefox()

    converter_url = 'http://www.sberbank.ru/ru/quotes/converter'
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
        self.driver.get(self.converter_url)
        wait = WebDriverWait(self.driver, self.timeout)
        wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME,
                                              self.locator_widgets_class)))

    def _filter_block(self):
        filter_block = self.driver.find_element_by_css_selector(
            self.locator_filter_block_css)
        return filter_block

    def _convert_block(self):
        filter_block = self._filter_block()
        convert_block = filter_block.find_element_by_css_selector(
            self.locator_convert_block_css)
        return convert_block

    def set_num_to_convert(self, num_to_convert):
        if not isinstance(num_to_convert, int):
            raise ValueError("Value for conversion should be int")

        convert_block = self._convert_block()

        num_input_form = convert_block.find_element_by_xpath(
            self.locator_num_input_xpath)
        num_input_form.clear()
        num_input_form.send_keys(num_to_convert)

    def set_currency_from_to(self, from_currency, to_currency):
        convert_block = self._convert_block()

        currency_selector_blocks = convert_block.find_elements_by_class_name(
            self.locator_currency_selector_block_class)
        from_currency_block = currency_selector_blocks[0]
        to_currency_block = currency_selector_blocks[1]

        # FROM
        from_currency_block.click()
        from_currency_dropdown = convert_block.find_element_by_css_selector(
            self.locator_currency_dropdown_css)
        from_currency_list = from_currency_dropdown.text.split()

        assert from_currency in from_currency_list, (
            "Provided currency is not in list of available variants: {0}"
            "".format(from_currency_list))

        from_currency_in_dropdown = (
            from_currency_dropdown.find_element_by_xpath(
                self.locator_currency_in_dropdown_xpath.format(
                    currency=from_currency)))
        from_currency_in_dropdown.click()

        # TO
        to_currency_block.click()
        to_currency_dropdown = convert_block.find_element_by_css_selector(
            self.locator_currency_dropdown_css)
        to_currency_list = to_currency_dropdown.text.split()

        assert to_currency in to_currency_list, (
            "Provided currency is not in list of available variants: {0}"
            "".format(to_currency_list))

        to_currency_in_dropdown = (
            to_currency_dropdown.find_element_by_xpath(
                self.locator_currency_in_dropdown_xpath.format(
                    currency=to_currency)))
        to_currency_in_dropdown.click()

    def click_apply_button(self):
        filter_block = self._filter_block()
        show_button = filter_block.find_element_by_xpath(
            self.locator_show_button_xpath)
        show_button.click()

    def get_results(self):
        wait = WebDriverWait(self.driver, self.timeout)
        result_form = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                                              self.locator_results_css)))

        # result_form = self.driver.find_element_by_css_selector(
        #     self.locator_results_css)
        return result_form.text


class TestConverter(ConverterPage):

    @pytest.yield_fixture(scope='session', autouse=True)
    def prepare(self):
        self.open_page()
        yield
        self.driver.close()

    def test_1(self):
        money = 123
        currency_from_to = 'RUR', 'CAD'

        with pytest.allure.step('step one'):
            self.set_num_to_convert(money)

        with pytest.allure.step('step two'):
            self.set_currency_from_to(currency_from_to[0], currency_from_to[1])

        with pytest.allure.step('step three'):
            self.click_apply_button()

        with pytest.allure.step('step four'):
            results = self.get_results()

        # import ipdb; ipdb.set_trace()
        # from IPython import embed; embed()

        assert str(money) in results
        assert all(i in results for i in currency_from_to)
