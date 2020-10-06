'''
	Created by Leema Rose.
	This mini test automates to validate applied filters on product list page
'''
import pytest
from read_excel import excel_to_dict
from config import TEST_DATA_FILE
from config import CALL_IT_SPRING_TITLE
from config import ALDO_TITLE

'''To inspect a test function and to generate tests according to test configuration or values specified in the class or module where a test function is defined.'''
def pytest_generate_tests(metafunc):
    argvalues = []
    for data in metafunc.cls.data:
        items = data.items()
        argnames = [x[0] for x in items]
        argvalues.append(([x[1] for x in items]))
    metafunc.parametrize(argnames, argvalues, scope="class")


@pytest.mark.usefixtures("driver_get")
class TestFiltering:
    data = excel_to_dict(TEST_DATA_FILE)
    
    '''To test the url gets loaded successfully'''
    def test_load_url(self, testcase_id, url, is_aldo_url, filter_by, perform, menu, gender, category, item, size, colour, price, expected_filter_count):
        self.driver.get(url)
        assert self.driver.title == ALDO_TITLE if is_aldo_url else CALL_IT_SPRING_TITLE
    
    '''To navigate to the menu items and ensures filter button is available'''
    def test_move_to_product_list_page_from_menu(self, testcase_id, url, is_aldo_url, filter_by, perform, menu, gender, category, item, size, colour, price, expected_filter_count):
        if filter_by.lower() == "menu":
            if perform.lower() == "click":
                self.page.click_action_button(self.driver, self.page.get_menu_xpath(menu))
                self.page.click_action_button(self.driver, self.page.get_shop_now_button_xpath(menu, gender, item, is_aldo_url))
            else:
                self.page.hover_on_menu_element(self.driver, menu, category, item)
        if filter_by.lower() == 'button':
            self.page.click_action_button(self.driver, self.page.get_shop_now_button_xpath(menu, gender, item, is_aldo_url, filter_by))
        
        filter_text = self.page.get_xpath_element(self.driver, self.page.FILTER_BUTTON_XPATH).text
        
        assert filter_text == 'Filter'
    
    '''To test if all the filter combinations applied'''
    def test_apply_filters(self, testcase_id, url, is_aldo_url, filter_by, perform, menu, gender, category, item, size, colour, price, expected_filter_count):
        self.page.click_dropdown_filter(self.driver, self.page.FILTER_BUTTON_XPATH)
        if filter_by.lower() == "menu" and perform.lower() == "click" and "men" not in menu.lower():
            filter_dict = {'Category': category, 'Size': size, 'Colour': colour, 'Price': price}
        elif filter_by.lower() == "button": 
            filter_dict = {'Category': item, 'Size': size, 'Colour': colour, 'Price': price}
        else:
            filter_dict = {'Size': size, 'Colour': colour, 'Price': price}    
            
        for key, value in filter_dict.items():
            if key.capitalize() in filter_dict and value is not None:
                print("key: %s and value: : %s" % (key, value))
                self.page.get_filter_selected(self.driver, key.capitalize(), value)
                
        self.driver.implicitly_wait(10)
        self.page.click_action_button(self.driver, self.page.get_apply_filter_xpath(is_aldo_url))
        
        actual_filter_count = self.page.get_applied_filter_count(self.driver, is_aldo_url)
        
        assert expected_filter_count == actual_filter_count   