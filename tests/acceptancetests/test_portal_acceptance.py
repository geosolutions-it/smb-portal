"""Acceptance tests for smb portal"""

import time

import pytest
import requests

pytestmark = pytest.mark.acceptance


def test_portal_available_at_url(browser, url):
    browser.visit(url)
    assert browser.title.lower().strip() == "save my bike"


@pytest.mark.skipif(
    vars(pytest.config.option).get("url", "").startswith("http://10.0.1"),
    reason="local dev setup does not use https"
)
def test_portal_http_request_redirects_to_https(browser, url):
    http_url = url.replace("http://", "https://")
    browser.visit(http_url)
    assert browser.url.startswith(url)


def test_on_first_visit_portal_displays_cookie_warning(browser, url):
    browser.visit(url)
    cookie_consent_div = browser.find_by_css("[aria-label=cookieconsent]")
    assert cookie_consent_div.visible


def test_cookie_warning_contains_link_to_privacy_policy(browser, url):
    browser.visit(url)
    privacy_policy_anchor = browser.find_by_css(
        ".cc-message > a.cc-link")
    assert privacy_policy_anchor["href"].endswith("/privacy_policy/")


def test_cookie_warning_disappears_after_acceptance(browser, url):
    browser.visit(url)
    consent_div_selector = "[aria-label=cookieconsent]"
    cookie_consent_div = browser.find_by_css(consent_div_selector)
    cookie_consent_accept_button = cookie_consent_div.find_by_css(
        ".cc-compliance > a")
    cookie_consent_accept_button.click()
    time.sleep(2)
    assert not cookie_consent_div.visible


def test_on_further_visits_portal_does_not_display_cookie_warning(browser,
                                                                  url):
    browser.visit(url)
    consent_div_selector = "[aria-label=cookieconsent]"
    cookie_consent_div = browser.find_by_css(consent_div_selector)
    cookie_consent_accept_button = cookie_consent_div.find_by_css(
        ".cc-compliance > a")
    cookie_consent_accept_button.click()
    browser.reload()
    assert not browser.find_by_css(consent_div_selector).visible


def test_portal_user_login_redirects_to_keycloak(browser, url,
                                                 keycloak_base_url):
    browser.visit(url)
    browser.execute_script(
        "document.querySelector('.account > .toolbar-dropdown > li > a')"
        ".click();")
    time.sleep(1)
    assert browser.url.startswith(keycloak_base_url)


def test_portal_user_is_able_to_register(browser, url, access_token):
    user_details = {
        "first_name": "Acceptance",
        "last_name": "Tester",
        "email": "acceptance.tester@mail.com",
        "password": "123456",
    }
    delete_user(url, user_details["email"], access_token)
    browser.visit(url)
    consent_div_selector = "[aria-label=cookieconsent]"
    browser.is_element_present_by_css(consent_div_selector, wait_time=10)

    # time.sleep(1)
    cookie_consent_div = browser.find_by_css(consent_div_selector)
    cookie_consent_accept_button = cookie_consent_div.find_by_css(
        ".cc-compliance > a")
    cookie_consent_accept_button.click()
    time.sleep(2)
    login_selector = ".account > .toolbar-dropdown > li > a"
    browser.execute_script(
        "document.querySelector('{}').click();".format(login_selector))
    go_register_css_selector = "#kc-registration > span > a"
    browser.is_element_present_by_css(go_register_css_selector, wait_time=30)
    click_element(browser, go_register_css_selector)
    browser.is_element_present_by_name("firstName", wait_time=10)
    browser.fill("firstName", user_details["first_name"])
    browser.fill("lastName", user_details["last_name"])
    browser.fill("email", user_details["email"])
    browser.fill("password", user_details["password"])
    browser.fill("password-confirm", user_details["password"])
    register_css_selector = "div#kc-form-buttons > input.btn-primary"
    browser.is_element_present_by_css(register_css_selector, wait_time=10)
    click_element(browser, register_css_selector)

    accept_tos_selector = "#id_accepted_terms_of_service"
    browser.is_element_present_by_css(accept_tos_selector, wait_time=10)
    scroll_to_element(browser, accept_tos_selector)
    browser.check("accepted_terms_of_service")
    time.sleep(1)
    click_element(browser, ".btn-primary")
    time.sleep(1)
    delete_user(url, user_details["email"], access_token)
    assert browser.url == "{}/it/profile/".format(url)


def click_element(browser, css_selector):
    """Click an element

    This function tries to scroll the element into view before clicking it

    """

    element_to_click = browser.find_by_css(css_selector)
    scroll_to_element(browser, css_selector)
    element_to_click.click()


def scroll_to_element(browser, query_selector):
    browser.driver.execute_script(
        "window.scrollTo(0, document.querySelector(arguments[0]"
        ").getBoundingClientRect().y)",
        query_selector
    )


def delete_user(base_url, email, access_token):
    headers = {
        "Authorization": "Bearer {}".format(access_token),
    }
    users_response = requests.get(
        "{}/api/users/".format(base_url),
        params={"email": email},
        headers=headers
    )
    users_response.raise_for_status()
    try:
        user_details = users_response.json()["results"][0]
    except IndexError:
        pass
    else:
        delete_response = requests.delete(
            "{}/api/users/{}/".format(base_url, user_details["uuid"]),
            headers=headers
        )
        delete_response.raise_for_status()


# tests = [
#     "keycloak login page allows accessing page for registering new user",
#     "after registering new user with keycloak, user is redirected
#     "back to portal",
#     "after logging in with keycloak, user is redirected back to portal",
#     "logged in user can access bikes list",
#     "anonymous user cannot access bikes list",
# ]
