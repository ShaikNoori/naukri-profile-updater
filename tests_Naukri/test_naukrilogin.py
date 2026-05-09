import os
import time
import traceback
import smtplib
from email.mime.text import MIMEText
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# =========================
# GITHUB SECRETS
# =========================

username = os.getenv("NAUKRI_USERNAME")
password = os.getenv("NAUKRI_PASSWORD")

sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")
receiver_email = os.getenv("RECEIVER_EMAIL")


# =========================
# EMAIL FUNCTION
# =========================

def send_email(subject, body):

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()

    server.login(sender_email, sender_password)

    server.sendmail(
        sender_email,
        receiver_email,
        msg.as_string()
    )

    server.quit()


# =========================
# MAIN FUNCTION
# =========================

def test_naukrid2dlogin():

    # =========================
    # CHROME OPTIONS
    # =========================

    options = uc.ChromeOptions()

    # Headless mode for GitHub Actions
    options.add_argument("--headless=new")

    # Disable save password popup
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2
    }

    options.add_experimental_option("prefs", prefs)

    # Browser options
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Required for GitHub Actions Linux
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # =========================
    # OPEN CHROME
    # =========================

    driver = uc.Chrome(
        options=options,
        use_subprocess=True
    )

    wait = WebDriverWait(driver, 30)

    try:

        # =========================
        # OPEN WEBSITE
        # =========================

        print("Opening Naukri website...")

        driver.get("https://www.naukri.com/")

        time.sleep(5)

        print("Website opened successfully")
        print("Current URL:", driver.current_url)
        print("Page Title:", driver.title)

        # =========================
        # CLICK LOGIN
        # =========================

        print("Finding Login button...")

        login_button = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "login_Layer")
            )
        )

        login_button.click()

        print("Clicked Login button")

        time.sleep(3)

        # =========================
        # USERNAME
        # =========================

        print("Entering username...")

        username_field = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//input[contains(@placeholder,'Email ID')]"
                )
            )
        )

        username_field.clear()

        username_field.send_keys(username)

        print("Username entered")

        # =========================
        # PASSWORD
        # =========================

        print("Entering password...")

        password_field = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//input[@type='password']"
                )
            )
        )

        password_field.clear()

        password_field.send_keys(password)

        print("Password entered")

        # =========================
        # LOGIN SUBMIT
        # =========================

        print("Clicking login submit button...")

        login_submit_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[@type='submit']"
                )
            )
        )

        login_submit_button.click()

        print("Login submitted")

        # =========================
        # WAIT AFTER LOGIN
        # =========================

        time.sleep(10)

        # =========================
        # CLOSE CHAT POPUP
        # =========================

        try:

            close_btn = driver.find_element(
                By.XPATH,
                "//span[contains(@class,'crossIcon')]"
            )

            driver.execute_script(
                "arguments[0].click();",
                close_btn
            )

            print("Chat popup closed")

        except:

            print("No chat popup found")

        # =========================
        # OPEN PROFILE DIRECTLY
        # =========================

        print("Opening profile page directly...")

        driver.get(
            "https://www.naukri.com/mnjuser/profile"
        )

        time.sleep(8)

        print("Profile page opened")

        # =========================
        # CLICK EDIT BUTTON
        # =========================

        print("Finding Edit button...")

        edit_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//em[text()='editOneTheme']"
                )
            )
        )

        driver.execute_script(
            "arguments[0].click();",
            edit_button
        )

        print("Edit button clicked")

        # =========================
        # WAIT FOR FORM
        # =========================

        time.sleep(5)

        # =========================
        # CLICK SAVE BUTTON
        # =========================

        print("Finding Save button...")

        save_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.ID,
                    "saveBasicDetailsBtn"
                )
            )
        )

        driver.execute_script(
            "arguments[0].click();",
            save_button
        )

        print("===================================")
        print("NAUKRI PROFILE UPDATED SUCCESSFULLY")
        print("===================================")

        # =========================
        # SEND SUCCESS EMAIL
        # =========================

        send_email(
            "Naukri Profile Updated Successfully",
            "Naukri profile updated successfully using GitHub Actions."
        )

        time.sleep(5)

    except Exception as e:

        print("\n===================================")
        print("ERROR OCCURRED")
        print("===================================")

        print(type(e).__name__)
        print(str(e))

        traceback.print_exc()

        driver.save_screenshot("error.png")

        print("\nScreenshot saved as error.png")

        # =========================
        # SEND FAILURE EMAIL
        # =========================

        send_email(
            "Naukri Automation Failed",
            f"""
Automation failed.

Error Type:
{type(e).__name__}

Error Message:
{str(e)}
"""
        )

    finally:

        driver.quit()

        print("Browser closed")


# =========================
# RUN SCRIPT
# =========================

if __name__ == "__main__":

    test_naukrid2dlogin()