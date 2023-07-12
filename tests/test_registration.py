import os
from datetime import datetime

import allure
from selene import command
from selene.support import by
from selene.support.conditions import have

from common_method import find_project_root
from src.base.user import User

directory = find_project_root()

user = User(
    first_name="first_name",
    last_name="last_name",
    email="email@hotmail.com",
    gender="Male",
    phone_number="1234567890",
    date_of_birth="23 July,1989",
    subject="Arts",
    interests="Sports",
    file="picture.jpg",
    current_address="current_address",
    state="NCR",
    city="Delhi",
)


@allure.title("Successful registration")
def test_registration_user(setup_browser):
    browser = setup_browser

    with allure.step("Open registrations form"):
        browser.open("https://demoqa.com/automation-practice-form")
        browser.element(".practice-form-wrapper").should(have.text("Student Registration Form"))
        browser.driver.execute_script("$('footer').remove()")
        browser.driver.execute_script("$('#fixedban').remove()")

    with allure.step("Fill form"):
        __dob = datetime.strptime(user.date_of_birth, "%d %B,%Y").date()

        browser.element("#firstName").type(user.first_name)
        browser.element("#lastName").type(user.last_name)
        browser.element(by.text(user.gender)).click()

        browser.element("#dateOfBirthInput").click()
        browser.element(".react-datepicker__month-select").type(__dob.month)
        browser.element(".react-datepicker__year-select").type(__dob.year)

        browser.element(
            f".react-datepicker__day--0{__dob.day}:not(.react-datepicker__day--outside-month)"
        ).click()

        browser.element("#userEmail").type(user.email)
        browser.element("#userNumber").type(user.phone_number)
        browser.element("#subjectsInput").send_keys(user.subject).press_enter()

        browser.element("#uploadPicture").send_keys(
            os.path.abspath(f"{directory}/data/file/{user.file}")
        )

        browser.element(by.text(user.interests)).click()

        browser.element("#currentAddress").type(user.current_address)

        browser.element("#state").perform(command.js.scroll_into_view).click()
        browser.element(f'//*[.="{user.state}"]').click()

        browser.element("#city").click()
        browser.element(f'//*[.="{user.city}"]').click()

        browser.element("#submit").perform(command.js.click)

    with allure.step("Assert form results"):
        browser.element("#example-modal-sizes-title-lg").should(have.text("Thanks for submitting the form"))
