import pytest

@pytest.fixture(scope="session")
def driver_get(request):
    from selenium import webdriver
    from page import Page
    web_driver = webdriver.Chrome(r"C:\Users\hari4\aldo-webui-python-selenium\chromedriver")
    web_driver.maximize_window()
    session = request.node
    page = Page()
    for item in session.items:
        cls = item.getparent(pytest.Class)
        setattr(cls.obj,"driver",web_driver)
        setattr(cls.obj,"page",page)
    yield
    web_driver.close()
    
@pytest.fixture(scope="class")
def driver_init(request):
    from selenium import webdriver
    from page import Page
    web_driver = webdriver.Chrome(r"C:\Users\hari4\aldo-webui-python-selenium\chromedriver")
    request.cls.driver = web_driver
    request.cls.page = Page()
    yield
    web_driver.close()
    
