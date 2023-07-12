import os
import allure
from datetime import datetime

from selene import be, command, have, by
from selene.support.shared import browser

from common_method import find_project_root

directory = find_project_root()


class RegistrationPage:

    @allure.step("Open registration page")
    def open(self):
        browser.open("https://demoqa.com/automation-practice-form/")

        # workaround how to remove appearing ads
        if (
                browser.all("[id^=google_ads][id$=container__]")
                        .with_(timeout=browser.config.timeout * 2)
                        .wait.until(have.size_greater_than_or_equal(3))
        ):
            browser.all("[id^=google_ads][id$=container__]").perform(command.js.remove)
        return self

    ##############################################################################

    @allure.step("Assert registration")
    def should_have_registered(self, user):
        user_info = [
            f"{user.first_name} {user.last_name}",
            user.email,
            user.gender,
            user.phone_number,
            user.date_of_birth,
            user.subject,
            user.interests,
            user.file,
            user.current_address,
            f"{user.state} {user.city}",
        ]

        browser.element("#example-modal-sizes-title-lg").should(be.visible).should(
            have.text("Thanks for submitting the form")
        )
        browser.all(".table").all("td:nth-of-type(2)").should(have.texts(user_info))
        return self

    @staticmethod
    @allure.step("Register user")
    def register(user):
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
