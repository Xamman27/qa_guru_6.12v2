import allure

from data.users import ihor
from src.pages.registration_page import RegistrationPage


@allure.title("Successful fill form")
def test_registration_user():
    registration_page = RegistrationPage()

    registration_page.open()
    registration_page.register(ihor)
    registration_page.should_have_registered(ihor)
