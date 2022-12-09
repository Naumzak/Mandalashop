from selenium.webdriver.common.by import By


class BaseLocators:
    """
    Locators that we see on all pages
    """
    LOGIN_LINK = (By.CSS_SELECTOR, "#login")
    CART_LINK = (By.CSS_SELECTOR, "#cart")
    SEARCH_LINK = (By.CSS_SELECTOR, "#search")
    LOGOUT_LINK = (By.CSS_SELECTOR, "#logout")
    CATEGORY_LINK = (By.CSS_SELECTOR, "#category")

    LOGO_LINK = (By.CSS_SELECTOR, ".logo")

class GoodsDetailLocators:
    IMAGE_PRODUCT_LINK = (By.CSS_SELECTOR, ".gallery_img")
    TARE_LINK = ( By.CSS_SELECTOR, "#tare")
    ADD_TO_CART_LINK = (By.TAG_NAME, "addtocart")
    QUANTITY_FIELD_LINK = (By.CSS_SELECTOR, "#quantity")
    AVAIBILITY_LINK = (By.CSS_SELECTOR, ".avaibility")


class MainPageLocators:
    """
    Locators for main page
    """
    SINGLE_CATEGORY_LINK = (By.CSS_SELECTOR, ".single-products-catagory")

class LoginPageLocators:
    """
    Locators for login page
    """
    REGISTER_FORM = (By.CSS_SELECTOR, "#register_form")
    LOGIN_FORM = (By.CSS_SELECTOR, "#login_form")


