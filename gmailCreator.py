from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import random
import time
import requests
from unidecode import unidecode
import uuid
from fp.fp import FreeProxy

from fake_useragent import UserAgent
from faker import Faker
import csv, os

ua = UserAgent()
fake = Faker()

def get_working_proxy():
    proxy = FreeProxy(rand=True, timeout=1).get()
    print(f"Using proxy: {proxy}")
    return proxy

def save_email_to_file(name, lastname, bday, email, password):

    filename='contas.csv'
    data = {
        'name': name,
        'lastname': lastname,
        'bday': bday,
        'email': email,
        'password': password
    }
    fileExists = os.path.exists(filename)
    
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'lastname', 'bday', 'email', 'password']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not fileExists:
            writer.writeheader()
        writer.writerow(data)

def generate_username(first_name, last_name):
    random_number = random.randint(1000, 9999)
    first_name_normalized = unidecode(first_name).lower()
    last_name_normalized = unidecode(last_name).lower()
    return f"{first_name_normalized}.{last_name_normalized}{random_number}"

def fill_form(driver):
    try:
        device_uuid = uuid.uuid4()
        print(f"Using device UUID: {device_uuid}")

        your_gender = "Prefiro não dizer"
        userFirstName = fake.first_name()
        userLastName = fake.last_name()
        your_username = generate_username(userFirstName, userLastName)
        your_password = fake.password()+"##$$%%^^&&"

        driver.get("https://accounts.google.com/signup/v2/createaccount?flowName=GlifWebSignIn&flowEntry=SignUp")

        first_name = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "firstName")))
        last_name = driver.find_element(By.NAME, "lastName")
        first_name.clear()
        first_name.send_keys(userFirstName)
        last_name.clear()
        last_name.send_keys(userLastName)

        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "VfPpkd-LgbsSe")))
        next_button.click()

        # Fill birthday and gender
        # wait = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "day")))
        dayInput = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "day")))
        if dayInput.is_displayed():
            year = random.randint(1940, 2005)
            day = random.randint(1,28)
            month_dropdown = driver.find_element(By.ID, "month")
            month_dropdown.click()
            month_dropdown = driver.find_element(By.CLASS_NAME,
            "MCs1Pd.HiC7Nc.VfPpkd-OkbHre.VfPpkd-aJasdd-RWgCYc-wQNmvb.VfPpkd-rymPhb-ibnC6b.VfPpkd-rymPhb-ibnC6b-OWXEXe-SfQLQb-Woal0c-RWgCYc")
            month_dropdown.click()

            # month_dropdown.select_by_value(birthday_elements[1])
            day_field = driver.find_element(By.ID, "day")
            day_field.click()
            day_field.clear()
            day_field.send_keys(day)
            year_field = driver.find_element(By.ID, "year")
            year_field.click()
            year_field.clear()
            year_field.send_keys(year)

            #gender
            wait = WebDriverWait(driver, 10)
            combo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#gender [role="combobox"]' )))
            if combo.get_attribute("aria-expanded") != "true":
                combo.click()

            # ul = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#gender [role="listbox"]')))
            # li = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#gender [role="listbox"] li[data-value="3"]')))
            
            xpath = f'//div[@id="gender"]//ul[@role="listbox"]//li[.//span[normalize-space()="{your_gender}"]]'
            li = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", li)
            try:
                li.click()
            except Exception:
                driver.execute_script("arguments[0].click();", li)
           
            time.sleep(2)
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "VfPpkd-LgbsSe")))
            next_button.click()
        else:
            print("Falou na data de nascimento")

        # Create custom email
        if driver.find_elements(By.ID, "selectionc22"):
            create_own_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "selectionc22")))
            create_own_option.click()

        create_own_email = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "Username")))
        username_field = driver.find_element(By.NAME, "Username")
        username_field.clear()
        username_field.send_keys(your_username)
        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "VfPpkd-LgbsSe")))
        next_button.click()

        # Enter and confirm password
        password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "Passwd")))
        password_field.clear()
        password_field.send_keys(your_password)
        confirm_passwd_div = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "confirm-passwd")))
        password_confirmation_field = confirm_passwd_div.find_element(By.NAME, "PasswdAgain")
        password_confirmation_field.clear()
        password_confirmation_field.send_keys(your_password)
        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "VfPpkd-LgbsSe")))
        next_button.click()

        # Skip phone number and recovery email
        try:
            skip_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Skip')]")))
            skip_button.click()
        except Exception as skip_error:
            print("No phone number verification step.")

        # Agree to terms
        agree_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button span.VfPpkd-vQzf8d")))
        agree_button.click()

        print(f"Your Gmail successfully created:\n{{\ngmail: {your_username}@gmail.com\npassword: {your_password}\n}}")
        bday=str(day)+'-'+'1'+'-'+str(year)
        save_email_to_file(userFirstName, userLastName, bday, f"{your_username}@gmail.com", your_password)

    except Exception as e:
        print("Failed to create your Gmail, Sorry")
        print(e)

# Create multiple accounts
def create_multiple_accounts(number_of_accounts):
    for i in range(number_of_accounts):
        chrome_options = Options()
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--user-data-dir=./cookies")
        user_agent = ua.random
        chrome_options.add_argument(f'user-agent={user_agent}')
        proxy = get_working_proxy()
        chrome_options.add_argument(f'--proxy-server={proxy}')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        # Caso seja necessario ajustar o tamanho da tela
        # driver.set_window_size(844, 390)
        # driver.set_window_size(390, 844)

        # Alterar a localização
        # lat = float(fake.latitude())
        # lon = float(fake.longitude())
        # driver.execute_cdp_cmd(
        #     "Emulation.setGeolocationOverride",
        #     {"latitude": lat, "longitude": lon, "accuracy": 100}
        # )

        fill_form(driver)
        driver.quit()
        time.sleep(random.randint(5, 15))

if __name__ == "__main__":
    number_of_accounts = 5
    create_multiple_accounts(number_of_accounts)
