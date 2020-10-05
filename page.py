from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

class Page:
    FILTER_BUTTON_XPATH = "//button//span[text()='Filter']"
    CLEAR_FILTER_BUTTON_XPATH = "//nav[contains(@class, 'outside')]//button/span[contains(text(), 'Clear filters')]"
    FILTER_INPUT_XPATH = "//input[@class='c-form-field-checkbox c-form-field-checkbox--has-mobile-list-display'][@id='%s-%s']"
    FILTER_LIST_OPTIONS_XPATH = ".//div[contains(@class, 'c-filter-group__body')]//ul/li//span[text()='%s']"
    APPLY_FILTER_BUTTON_XPATH = "//nav[contains(@class, 'outside')]//button/span[contains(text(), 'Apply')]"
    APPLIED_FILTER_COUNT_XPATH = "//button[contains(@class, 'filters__filter-applied')]"
    ALDO_URL = "https://www.aldoshoes.com"
    CALLITSPRING_URL = "https://www.callitspring.com"
    LIST_ITEM_FILTERS = ['Size', 'Colour']
    INPUT_ITEM_FILTERS = ['Category', 'Price', 'Heel-Height']
    TEST_DATA_FILE = "C:\\Users\\hari4\\aldo-webui-python-selenium\\Aldo-Test-Data_V5.xlsx"
    FILTER_DROPDOWN_XPATH = "//button//span[text()='Hide']"
    ITEM_XPATH_FROM_SUB_MENU = "//a[@class='c-navigation__link']['/%s/%s/'][text()='%s']"
    SUB_MENU_XPATH = "//ul//li/a[contains(@href, '/%s/')]//span[@class='u-text-nowrap'][text()='%s']" 
    NEW_ARRIVAL_MENU_XPATH = "//div[contains(@class, 'c-header-container--sticky')]//ul//li//span[@class='u-btn__content']/span[text()='New arrivals']"
    MENU_XPATH_OTHER_THAN_NEW_ARRIVAL = "//div[contains(@class, 'c-header-container--sticky')]//ul//li//span[@class='u-btn__content']/span[text()='%s']"
    SHOP_NOW_BUTTON_XPATH = "//a[contains(@href, '/%s/')][text()='Shop now']"
    SHOP_ITEM_BUTTON_XPATH = "//div[contains(@class, 'is-active')]//a[text()='Shop %s']"
    SHOP_BY_GENDER_BUTTON_XAPTH = "//a[text()='Shop %s']"
    
    def get_menu_xpath(menu):
        if menu.lower() == "new arrivals":
            return Page.NEW_ARRIVAL_MENU_XPATH
        else:
            return Page.MENU_XPATH_OTHER_THAN_NEW_ARRIVAL % (menu)
    
    def get_drop_down_item(gender, category):
        return Page.DROP_DOWN_LIST % (gender.lower(), category.lower(), category.capitalize())
        
    def get_filter_selected(driver, key, value):
        if key in Page.LIST_ITEM_FILTERS:
            filter_xpath = Page.FILTER_LIST_OPTIONS_XPATH % (value)
            Page.click_action_button(driver, filter_xpath)
        else:
            filter_xpath = Page.FILTER_INPUT_XPATH % (key.lower(), value.replace(" ", "").lower())
            Page.check_or_uncheck_box(driver, filter_xpath)

    def get_shop_now_button_xpath(menu, gender, item):
        if menu.replace(" ", "-").lower() in ('new-arrivals', 'sale'):
            shop_button_xpath = Page.SHOP_NOW_BUTTON_XPATH % (gender.lower())
        elif menu.lower() in ('men', 'women'):
            shop_button_xpath = Page.SHOP_ITEM_BUTTON_XPATH % (item.lower())
        else:
            shop_button_xpath = Page.SHOP_BY_GENDER_BUTTON_XAPTH % (gender.lower())
        return shop_button_xpath
    
    def click_action_button(driver, item_xpath):
        wait = WebDriverWait(driver, 10)
        print("Clicking on %s" % item_xpath)
        try:
            button_element = wait.until(EC.element_to_be_clickable((By.XPATH, item_xpath)))
            ActionChains(driver).click(button_element).perform()
        except TimeoutException:
            print("Loading took too much time!")
        
    def click_dropdown_filter(driver, item_xpath):
        wait = WebDriverWait(driver, 10)
        print("Clicking on %s" % item_xpath)
        try:
            button_element = wait.until(EC.element_to_be_clickable((By.XPATH, item_xpath)))
            driver.execute_script("arguments[0].click()", button_element)
        except TimeoutException:
            print("Loading took too much time!")

    def check_or_uncheck_box(driver, item_xpath):
        print("Clicking on %s" % item_xpath)
        checkbox = driver.find_element(By.XPATH, item_xpath)
        Page.scroll_element_into_view(driver, checkbox)
        
    def scroll_element_into_view(driver, element):
        """Scroll element into view"""
        y = element.location['y']
        driver.execute_script('window.scrollTo(0, {0})'.format(y))
        driver.implicitly_wait(10)
        driver.execute_script("arguments[0].click()", element)
        
    def hover_on_menu_element(driver, menu, category, item):
        wait = WebDriverWait(driver, 10)
        print("menu xpath : %s" % Page.get_menu_xpath(menu))
        menu_hover_element = wait.until(EC.element_to_be_clickable((By.XPATH, Page.get_menu_xpath(menu))))
        ActionChains(driver).move_to_element(menu_hover_element).perform()
        
        print("item from submenu xpath : %s" %  Page.ITEM_XPATH_FROM_SUB_MENU % (menu.lower(), category.lower(), item))
        click_sub_menu_item_element = wait.until(EC.element_to_be_clickable((By.XPATH, Page.ITEM_XPATH_FROM_SUB_MENU % (menu.lower(), category.lower(), item))))
        driver.execute_script("arguments[0].click()", click_sub_menu_item_element)
        
    def get_xpath_element(driver, item_xpath):
        wait = WebDriverWait(driver, 10)
        web_element = wait.until(EC.presence_of_element_located((By.XPATH, item_xpath)))
        return web_element
    
    def get_xpath_all_elements(driver, item_xpath):
        wait = WebDriverWait(driver, 10)
        web_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, item_xpath)))
        return web_elements
    