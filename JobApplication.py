from tkinter import Tk, scrolledtext, Button
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def input_cover_letter():
    cover_letter_window = Tk()
    cover_letter_window.title("Cover Letter")
    cover_letter_window.geometry("400x300")

    cover_letter_text = scrolledtext.ScrolledText(cover_letter_window, wrap='word', width=40, height=15)
    cover_letter_text.pack(expand=True, fill='both')

    def submit():
        global cover_letter_input
        cover_letter_input = cover_letter_text.get("1.0", "end-1c")
        cover_letter_window.destroy()

    submit_button = Button(cover_letter_window, text="Submit", command=submit)
    submit_button.pack()

    cover_letter_window.mainloop()

def login_process(email, password):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.startupjobs.cz")

    try:
        cookie_button_xpath = '//button[text()="Přijmout"]'
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, cookie_button_xpath))
        ).click()
        login_button_xpath = '//button[text()="Přihlásit se"]'
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, login_button_xpath))
        ).click()
        email_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        email_field.send_keys(email)
        continue_button_xpath = '//button[text()="Pokračovat"]'
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, continue_button_xpath))
        ).click()
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "password"))
        )
        password_field.send_keys(password)
        login_button = driver.find_element(By.XPATH, '//button[text()="Přihlásit"]')
        login_button.click()

        return driver

    except Exception as e:
        print(f"An error occurred during login: {e}")
        return None

def fill_job_application(driver, job_application_url, cover_letter_text):
    try:
        driver.get(job_application_url)
        nabidka_button_xpath = '//button[text()="Mám zájem o nabídku"]'
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, nabidka_button_xpath))
        ).click()
        cover_letter_input_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@contenteditable="true"]'))
        )
        cover_letter_input_field.send_keys(cover_letter_text)
        checkbox = driver.find_element(By.ID, "attachment-0")
        checkbox.click()

        return True

    except Exception as e:
        print(f"An error occurred during job application: {e}")
        return False

def main():
    email = "useyourownadress@seznam.cz"
    password = "heslo123"
    print("Input cover letter")
    input_cover_letter()
    print("Cover letter text submitted successfully.")
    print("Login process")
    driver = login_process(email, password)
    if driver:
        print("Login successful.")
    else:
        print("Login failed.")
        return

    while True:
        job_application_url = input("Please enter the job application URL: ")
        print("Filling up the job application")
        if fill_job_application(driver, job_application_url, cover_letter_input):
            print("Job application filled successfully.")
        else:
            print("Failed to fill job application.")
            continue

        confirmation = input("Hit Enter to send this job application: ")
        if confirmation.lower() == "exit":
            break
        else:
            odeslat_button_xpath = '//button[text()="Odeslat zájem"]'
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, odeslat_button_xpath))
            ).click()
            print("Job application sent successfully.")

    driver.quit()

if __name__ == "__main__":
    main()
