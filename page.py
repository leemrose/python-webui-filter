from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

class Page:
    """XPATH Constants for the page"""
    
    FILTER_BUTTON_XPATH = "//button//span[text()='Filter']"
    APPLIED_FILTER_BUTTON_XPATH = "//button//span[contains(text(), 'Filter ( ')]"
    CLEAR_FILTER_BUTTON_XPATH = "//nav[contains(@class, 'outside')]//button/span[contains(text(), 'Clear filters')]"
    FILTER_INPUT_XPATH = "//input[@class='c-form-field-checkbox c-form-field-checkbox--has-mobile-list-display'][@id='%s-%s']"
    FILTER_LIST_OPTIONS_XPATH = ".//div[contains(@class, 'c-filter-group__body')]//ul/li//span[text()='%s']"
    APPLY_ALDO_FILTER_BUTTON_XPATH = "//nav[contains(@class, 'outside')]//button/span[contains(text(), 'Apply')]"
    APPLY_FILTER_BUTTON_XPATH = "//nav[contains(@class, 'desktop')]//button/span[contains(text(), 'Apply')]"
    APPLIED_FILTER_COUNT_XPATH = "//button[contains(@class, 'filters__filter-applied')]"
    LIST_ITEM_FILTERS = ['Size', 'Colour']
    INPUT_ITEM_FILTERS = ['Category', 'Price', 'Heel-Height']
    TEST_DATA_FILE = "C:\\Users\\hari4\\python-webui-filter\\Aldo-Test-Data.xlsx"
    FILTER_DROPDOWN_XPATH = "//button//span[text()='Hide']"
    ITEM_XPATH_FROM_SUB_MENU = "//div[@aria-labelledby='regular-menu-caen%s']//a[@class='c-navigation__link'][text()='%s']"
    NEW_ARRIVAL_MENU_XPATH = "//nav[contains(@class, 'c-header')]//span[@class='u-btn__content']/span[text()='New arrivals']"
    MENU_XPATH_OTHER_THAN_NEW_ARRIVAL = "//button[@id='regular-menu-caen%s']//span[@class='u-btn__content']/span[text()='%s']"
    SHOP_NOW_BUTTON_XPATH = "//a[contains(@href, '/%s/')][text()='Shop now']"
    SHOP_ITEM_BUTTON_XPATH = "//div[contains(@class, 'is-active')]//a[text()='Shop %s']"
    SHOP_BY_GENDER_BUTTON_XAPTH = "//a[text()='Shop %s']"
    
    def get_menu_xpath(self, menu):
        if menu.lower() == "new arrivals":
            return self.NEW_ARRIVAL_MENU_XPATH
        else:
            return self.MENU_XPATH_OTHER_THAN_NEW_ARRIVAL % (menu.lower(), menu)
        
    def get_apply_filter_xpath(self, is_aldo_url):
        return self.APPLY_FILTER_BUTTON_XPATH if not is_aldo_url else self.APPLY_ALDO_FILTER_BUTTON_XPATH
    
    def get_filter_selected(self, driver, key, value):
        if key in self.LIST_ITEM_FILTERS:
            filter_xpath = self.FILTER_LIST_OPTIONS_XPATH % (value)
            self.click_list_option_button(driver, filter_xpath)
        else:
            filter_xpath = self.FILTER_INPUT_XPATH % (key.lower(), value.replace(" ", "").replace(".", "").replace("$", "").lower())
            self.check_or_uncheck_box(driver, filter_xpath)

    def click_list_option_button(self, driver, item_xpath):
        wait = WebDriverWait(driver, 10)
        print("Clicking on %s" % item_xpath)
        try:
            list_option_element = wait.until(EC.element_to_be_clickable((By.XPATH, item_xpath)))
            driver.implicitly_wait(10)
            driver.execute_script("arguments[0].click()", list_option_element)
#            ActionChains(driver).click(button_element).perform()
        except TimeoutException:
            print("Loading took too much time!")
            
    def get_shop_now_button_xpath(self, menu, gender, item, is_aldo_url, filter_by):
        if menu.replace(" ", "-").lower() in ('new-arrivals', 'sale') and is_aldo_url:
            shop_button_xpath = self.SHOP_NOW_BUTTON_XPATH % (gender.lower())
        elif menu.lower() in ('men', 'women') and filter_by.lower() == "click":
            shop_button_xpath = self.SHOP_ITEM_BUTTON_XPATH % (item.lower())
        elif menu.lower() == 'Sale' and not is_aldo_url:
            shop_button_xpath = self.SHOP_BY_GENDER_BUTTON_XAPTH % (gender.lower())
        else:
            gender = gender.lower() if is_aldo_url else gender 
            shop_button_xpath = self.SHOP_BY_GENDER_BUTTON_XAPTH % (gender)
        return shop_button_xpath
    
    def click_action_button(self, driver, item_xpath):
        wait = WebDriverWait(driver, 10)
        print("Clicking on %s" % item_xpath)
        try:
            button_element = wait.until(EC.element_to_be_clickable((By.XPATH, item_xpath)))
            ActionChains(driver).click(button_element).perform()
        except TimeoutException:
            print("Loading took too much time!")
        
    def click_dropdown_filter(self, driver, item_xpath):
        wait = WebDriverWait(driver, 10)
        print("Clicking on %s" % item_xpath)
        try:
            button_element = wait.until(EC.element_to_be_clickable((By.XPATH, item_xpath)))
#            self.scroll_element_into_view(driver, button_element)
            driver.execute_script("arguments[0].click()", button_element)
        except TimeoutException:
            print("Loading took too much time!")
        driver.implicitly_wait(10)

    def check_or_uncheck_box(self, driver, item_xpath):
        print("Clicking on %s" % item_xpath)
        checkbox = driver.find_element(By.XPATH, item_xpath)
        self.scroll_element_into_view(driver, checkbox)
        
    def scroll_element_into_view(self, driver, element):
        """Scroll element into view"""
        y = element.location['y']
        driver.execute_script('window.scrollTo(0, {0})'.format(y))
        driver.implicitly_wait(10)
        driver.execute_script("arguments[0].click()", element)
        
    def hover_on_menu_element(self, driver, menu, category, item):
        wait = WebDriverWait(driver, 10)
        print("menu xpath : %s" % self.get_menu_xpath(menu))
        menu_hover_element = wait.until(EC.element_to_be_clickable((By.XPATH, self.get_menu_xpath(menu))))
        ActionChains(driver).move_to_element(menu_hover_element).perform()
        
        print("item from submenu xpath : %s" %  self.ITEM_XPATH_FROM_SUB_MENU % (menu.lower(), item))
        click_sub_menu_item_element = wait.until(EC.element_to_be_clickable((By.XPATH, self.ITEM_XPATH_FROM_SUB_MENU % (menu.lower(), item))))
        driver.execute_script("arguments[0].click()", click_sub_menu_item_element)
        
    def get_xpath_element(self, driver, item_xpath):
        wait = WebDriverWait(driver, 10)
        web_element = wait.until(EC.presence_of_element_located((By.XPATH, item_xpath)))
        return web_element
    
    def get_xpath_all_elements(self, driver, item_xpath):
        wait = WebDriverWait(driver, 10)
        web_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, item_xpath)))
        return web_elements
    
    def get_applied_filter_count(self, driver, is_aldo_url):
        if is_aldo_url:
            return len(self.get_xpath_all_elements(driver, self.APPLIED_FILTER_COUNT_XPATH))
        else:
            return int((self.get_xpath_element(driver, self.APPLIED_FILTER_BUTTON_XPATH).text).split(" ")[2])