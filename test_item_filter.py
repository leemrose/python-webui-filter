import pytest
from selenium import webdriver
from page import Page
from read_excel import excelToDict 

test_inputs = excelToDict(Page.TEST_DATA_FILE)

@pytest.fixture(scope="class")
def driver_init(request):
    web_driver = webdriver.Chrome(r"C:\Users\hari4\aldo-webui-python-selenium\chromedriver")
    web_driver.maximize_window()
    request.cls.driver = web_driver
    yield
    web_driver.close()
    

@pytest.mark.usefixtures("driver_init")
@pytest.mark.parametrize("testcase_id, url, filter_by, perform, menu, gender, category, item, size, colour, price, expected_filter_count", test_inputs)
class TestFiltering:
    
    def test_load_url(self, testcase_id, url, filter_by, perform, menu, gender, category, item, size, colour, price, expected_filter_count):
        self.driver.get(Page.ALDO_URL)
        assert self.driver.title == "ALDO Canada | ALDO Shoes, Boots, Sandals, Handbags and Accessories"

    def test_move_to_product_list_page_from_menu(self, testcase_id, url, filter_by, perform, menu, gender, category, item, size, colour, price, expected_filter_count):
        
        if filter_by.lower() == 'menu':
            if perform.lower() == 'click':
                print("Inside Menu Click function")
                Page.click_action_button(self.driver, Page.get_menu_xpath(menu))
                Page.click_action_button(self.driver, Page.get_shop_now_button_xpath(menu, gender, item))
            else:
                print("Inside Menu Hover function")
                Page.hover_on_menu_element(self.driver, menu, category, item)
        if filter_by.lower() == 'button':
            print("Inside Button Click function")
            Page.click_action_button(self.driver, Page.get_shop_now_button_xpath(menu, gender, item))
        
        filter_text = Page.get_xpath_element(self.driver, Page.FILTER_BUTTON_XPATH).text
        
        assert filter_text == 'Filter'
                
    def test_apply_filters(self, testcase_id, url, filter_by, perform, menu, gender, category, item, size, colour, price, expected_filter_count):
        Page.click_dropdown_filter(self.driver, Page.FILTER_BUTTON_XPATH)

        if filter_by.lower() == "menu" and perform.lower() == "click" and "men" not in menu.lower():
            filter_dict = {'Category': category, 'Size': size, 'Colour': colour, 'Price': price}
        elif filter_by.lower() == "button": 
            filter_dict = {'Category': item, 'Size': size, 'Colour': colour, 'Price': price}
        else:
            filter_dict = {'Size': size, 'Colour': colour, 'Price': price}    
            
        for key, value in filter_dict.items():
            if key.capitalize() in filter_dict and value is not None:
                print("key: %s and value: : %s" % (key, value))
                Page.get_filter_selected(self.driver, key.capitalize(), value)
        
        Page.click_action_button(self.driver, Page.APPLY_FILTER_BUTTON_XPATH)
        filter_elements = Page.get_xpath_all_elements(self.driver, Page.APPLIED_FILTER_COUNT_XPATH)
        assert expected_filter_count == len(filter_elements)   