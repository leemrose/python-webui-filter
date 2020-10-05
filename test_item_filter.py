import pytest
from read_excel import excelToDict

def pytest_generate_tests(metafunc):
    argvalues = []
    for data in metafunc.cls.data:
        items = data.items()
        argnames = [x[0] for x in items]
        argvalues.append(([x[1] for x in items]))
    metafunc.parametrize(argnames, argvalues, scope="class")


@pytest.mark.usefixtures("driver_get")
class TestFiltering:
    data = excelToDict("C:\\Users\\hari4\\python-webui-filter\\Aldo-Test-Data1.xlsx")
    
    def test_load_url(self, testcase_id, url, is_aldo_url, filter_by, perform, menu, gender, category, item, size, colour, price, expected_filter_count):
        self.driver.get(url)
        print("running load url test ")
        assert self.driver.title == "ALDO Canada | ALDO Shoes, Boots, Sandals, Handbags and Accessories" if is_aldo_url else " Call It Spring Canada | Vegan Shoes, Boots, Sandals & Handbags"

    def test_move_to_product_list_page_from_menu(self, testcase_id, url, is_aldo_url, filter_by, perform, menu, gender, category, item, size, colour, price, expected_filter_count):
        print("running for finding filter")    
        if filter_by.lower() == 'menu':
            if perform.lower() == 'click':
                print("Inside Menu Click function")
                self.page.click_action_button(self.driver, self.page.get_menu_xpath(menu))
                self.page.click_action_button(self.driver, self.page.get_shop_now_button_xpath(menu, gender, item, is_aldo_url))
            else:
                print("Inside Menu Hover function")
                self.page.hover_on_menu_element(self.driver, menu, category, item)
        if filter_by.lower() == 'button':
            print("Inside Button Click function")
            self.page.click_action_button(self.driver, self.page.get_shop_now_button_xpath(menu, gender, item, is_aldo_url, filter_by))
        
        filter_text = self.page.get_xpath_element(self.driver, self.page.FILTER_BUTTON_XPATH).text
        
        assert filter_text == 'Filter'
    
    def test_apply_filters(self, testcase_id, url, is_aldo_url, filter_by, perform, menu, gender, category, item, size, colour, price, expected_filter_count):
        print("running for applying filter")
        self.page.click_dropdown_filter(self.driver, self.page.FILTER_BUTTON_XPATH)
        print(testcase_id, url, is_aldo_url, filter_by, perform, menu, gender, category, item, size, colour, price, expected_filter_count)
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
        print("filter_count value is : %s" % actual_filter_count)
        
        assert expected_filter_count == actual_filter_count   