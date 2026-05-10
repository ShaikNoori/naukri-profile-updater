import gc
import os
import time
import traceback
import smtplib

from email.mime.text import MIMEText

import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# =========================================================
# GITHUB SECRETS
# =========================================================
# These values come securely from GitHub Actions Secrets
# Repository -> Settings -> Secrets and variables -> Actions
# =========================================================

# =========================
# LOCAL CREDENTIALS
# =========================

# =========================
# CREDENTIALS
# =========================

username = os.getenv("NAUKRI_USERNAME") or "noori.shaiknowreen@gmail.com"
password = os.getenv("NAUKRI_PASSWORD") or "43Zindagi@noori"
sender_email = os.getenv("SENDER_EMAIL") or "noori.shaiknowreen@gmail.com"
sender_password = os.getenv("SENDER_PASSWORD") or "eirl dcgp gsoc crqr"
receiver_email = os.getenv("RECEIVER_EMAIL") or "noori.shaiknowreen@gmail.com"


# =========================================================
# EMAIL FUNCTION
# =========================================================
# Sends email notification after success/failure
# =========================================================

def send_email(subject, body):

    try:

        # Create email message
        msg = MIMEText(body)

        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email

        # Connect to Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)

        # Start TLS encryption
        server.starttls()

        # Login to Gmail
        server.login(sender_email, sender_password)

        # Send email
        server.sendmail(
            sender_email,
            receiver_email,
            msg.as_string()
        )

        # Close server connection
        server.close()

        print("Email sent successfully")

    except Exception as email_error:

        print("Failed to send email")
        print(str(email_error))


# =========================================================
# MAIN AUTOMATION FUNCTION
# =========================================================

def test_naukrid2dlogin():

    driver = None

    try:

        # =========================================================
        # VALIDATE GITHUB SECRETS
        # =========================================================

        if not username or not password:
            raise Exception(
                "Naukri credentials missing in GitHub Secrets"
            )

        if not sender_email or not sender_password or not receiver_email:
            raise Exception(
                "Email credentials missing in GitHub Secrets"
            )

        # =========================================================
        # CHROME OPTIONS
        # =========================================================

        options = uc.ChromeOptions()

        # Headless mode for GitHub Actions
        # Browser runs in background without UI
        options.add_argument("--headless=new")

        # Stability options for Linux GitHub runner
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        # Browser size
        options.add_argument("--window-size=1920,1080")

        # Disable browser features/popups
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-extensions")

        # Helps reduce automation detection
        options.add_argument(
            "--disable-blink-features=AutomationControlled"
        )

        # Disable password manager popup
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2
        }

        options.add_experimental_option("prefs", prefs)

        # =========================================================
        # OPEN CHROME BROWSER
        # =========================================================

        print("Launching Chrome browser...")

        driver = uc.Chrome(
          #  version_main=147,
            options=options,
            use_subprocess=True
        )

        # Explicit wait object
        wait = WebDriverWait(driver, 30)

        # =========================================================
        # OPEN NAUKRI WEBSITE
        # =========================================================

        print("Opening Naukri website...")

        driver.get("https://www.naukri.com/")

        time.sleep(5)

        print("Website opened successfully")
        print("Current URL:", driver.current_url)
        print("Page Title:", driver.title)

        # =========================================================
        # CLICK LOGIN BUTTON
        # =========================================================

        print("Finding Login button...")

        login_button = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "login_Layer")
            )
        )

        login_button.click()

        print("Clicked Login button")

        time.sleep(3)

        # =========================================================
        # ENTER USERNAME
        # =========================================================

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

        print("Username entered successfully")

        # =========================================================
        # ENTER PASSWORD
        # =========================================================

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

        print("Password entered successfully")

        # =========================================================
        # CLICK LOGIN SUBMIT BUTTON
        # =========================================================

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

        print("Login submitted successfully")

        # Wait after login
        time.sleep(10)

        # =========================================================
        # CLOSE CHAT POPUP IF PRESENT
        # =========================================================

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

        # =========================================================
        # OPEN PROFILE PAGE DIRECTLY
        # =========================================================

        print("Opening profile page...")

        driver.get(
            "https://www.naukri.com/mnjuser/profile"
        )

        time.sleep(8)

        print("Profile page opened successfully")

        # =========================================================
        # CLICK EDIT BUTTON
        # =========================================================

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

        # Wait for form
        time.sleep(5)

        # =========================================================
        # CLICK SAVE BUTTON
        # =========================================================

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

        # =========================================================
        # SEND SUCCESS EMAIL
        # =========================================================

        send_email(
            "Naukri Profile Updated Successfully",
            """
Naukri profile updated successfully using GitHub Actions.

Automation Status:
SUCCESS
"""
        )

        time.sleep(5)

    except Exception as e:

        print("\n===================================")
        print("ERROR OCCURRED")
        print("===================================")

        print(type(e).__name__)
        print(str(e))

        traceback.print_exc()

        # =========================================================
        # SAVE ERROR SCREENSHOT
        # =========================================================

        try:

            if driver:

                driver.save_screenshot("error.png")

                print("Screenshot saved as error.png")

        except:

            print("Unable to save screenshot")

        # =========================================================
        # SEND FAILURE EMAIL
        # =========================================================

        send_email(
            "Naukri Automation Failed",
            f"""
Naukri automation failed.

Error Type:
{type(e).__name__}

Error Message:
{str(e)}
"""
        )

        raise

    finally:

        try:
            if driver:
                driver.quit()
                print("Browser closed")

        except Exception:
            pass

        gc.collect()


# =========================================================
# RUN SCRIPT
# =========================================================

if __name__ == "__main__":

    test_naukrid2dlogin()