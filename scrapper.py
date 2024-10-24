from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
import logging
import time


logging.basicConfig(level=logging.DEBUG,
                    filename='C:\\Users\\kules\\Desktop\\scrapper\\scraper.log',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')


driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))


timeout = 5  

def get_restaurant_urls(base_url):
    try:
        driver.get(base_url)

        restaurant_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/pl/pol/warsaw/restaurant/')]")
        urls = [link.get_attribute('href') for link in restaurant_links]

        logging.info(f'Znaleziono {len(urls)} restauracji.')
        return urls
    except Exception as err:
        logging.error(f'Niespodziewany błąd: {err}')
        return []


def get_menu_for_restaurant(restaurant_url):
    categories = {}

    try:
        driver.get(restaurant_url)

        category_sections = WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@data-test-id='MenuSection']"))
        )

        for section in category_sections:

            category_name = section.find_element(By.XPATH, ".//h2").text.strip()

  
            dishes = section.find_elements(By.XPATH, ".//div[@data-test-id='horizontal-item-card']")
            menu = {}
            for dish in dishes:
                title_element = dish.find_element(By.XPATH, ".//h3[@data-test-id='horizontal-item-card-header']")
                price_elements = dish.find_elements(By.XPATH, ".//span[contains(@class, 'sc-') and contains(@aria-label, 'Cena')]")
                dish_name = title_element.text.strip()
                dish_price = ' '.join([price_elem.text for price_elem in price_elements if price_elem.text.strip() != ''])
                menu[dish_name] = dish_price

            if menu:
                categories[category_name] = menu

        logging.info(f'Znaleziono {len(categories)} kategorii w restauracji {restaurant_url}.')
        return categories

    except TimeoutException as te:
        logging.error(f'Czas oczekiwania na sekcje menu wygasł dla {restaurant_url}: {te}')
    except Exception as e:
        logging.error(f'Niespodziewany błąd przy przetwarzaniu {restaurant_url}: {e}')

    return categories


def get_rating(restaurant_url):
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span[class*='sc-4114a3cc-2']"))
        )
        rating_tag = driver.find_element(By.CSS_SELECTOR, "span[class*='sc-4114a3cc-2']")
        rating = rating_tag.text.strip()
        logging.info(f'Znaleziono ocenę dla restauracji {restaurant_url}: {rating}.')
        return rating
    except TimeoutException:
        logging.error(f'Czas oczekiwania na ocenę wygasł dla restauracji {restaurant_url}.')
        return ""
    except NoSuchElementException:
        logging.error(f'Nie znaleziono elementu oceny dla restauracji {restaurant_url}.')
        return ""
    except Exception as err:
        logging.error(f'Niespodziewany błąd przy przetwarzaniu oceny dla {restaurant_url}: {err}')
        return ""




def get_address(restaurant_url):
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'sc-362cd990-0')]//p[contains(@class, 'sc-347bbdf5-3')]"))
        )
        address_tag = driver.find_element(By.XPATH, "//div[contains(@class, 'sc-362cd990-0')]//p[contains(@class, 'sc-347bbdf5-3')]")
        address = address_tag.text.strip()
        logging.info(f'Znaleziono adres dla restauracji {restaurant_url}: {address}.')
        return address
    except TimeoutException:
        logging.error(f'Czas oczekiwania na adres wygasł dla restauracji {restaurant_url}.')
        return ""
    except NoSuchElementException:
        logging.error(f'Nie znaleziono elementu adresu dla restauracji {restaurant_url}.')
        return ""
    except Exception as err:
        logging.error(f'Niespodziewany błąd przy przetwarzaniu adresu dla {restaurant_url}: {err}')
        return ""


def close_cookie_banner():
    try:
        accept_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ConsentsBannerOverlay')]//button[contains(., 'Akceptuj')]"))
        )
        accept_button.click()
        logging.info("Baner cookie został zamknięty.")
    except TimeoutException:
        logging.error("Baner cookie nie pojawił się w czasie oczekiwania.")
    except NoSuchElementException:
        logging.info("Baner cookie nie został znaleziony.")
    except Exception as e:
        logging.error(f'Wystąpił błąd przy próbie zamknięcia baneru cookie: {e}')



def get_description(restaurant_url):
    try:
        driver.get(restaurant_url)
        close_cookie_banner()
        details_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test-id='venue-more-info-button']"))
        )
        details_button.click()

        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-test-id='VenueInformationModal']"))
        )

        description_tag = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[@data-test-id='VenueLargeHeader']/following-sibling::p"))
        )
        description = description_tag.text.strip()
        logging.info(f'Znaleziono opis dla restauracji {restaurant_url}: {description}.')
        return description
    except TimeoutException:
        logging.error(f'Czas oczekiwania na opis wygasł dla restauracji {restaurant_url}.')
        return ""
    except NoSuchElementException:
        logging.error(f'Nie znaleziono opisu dla restauracji {restaurant_url}.')
        return ""
    except Exception as err:
        logging.error(f'Niespodziewany błąd przy pobieraniu opisu dla {restaurant_url}: {err}')
        return ""




def scroll_to_contact_section():
    try:
        contact_header = driver.find_element(By.XPATH, "//h3[contains(text(), 'Informacje o dostawie')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", contact_header)
        time.sleep(3)
        logging.info("Przewinięto do sekcji 'Kontakt'.")
    except NoSuchElementException:
        logging.error("Nie znaleziono sekcji 'Kontakt'.")
    except Exception as e:
        logging.error(f"Wystąpił błąd podczas przewijania do sekcji 'Kontakt': {e}")



def get_delivery_info(restaurant_url):
    delivery_info = {'hours': {}, 'details': {}}
    try:
        delivery_info_modal = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-test-id='VenueInformationModal']"))
        )

        scroll_to_contact_section()

        delivery_hours_rows = delivery_info_modal.find_elements(
            By.CSS_SELECTOR, "h3+table tr"
        )
        for row in delivery_hours_rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            if len(cells) == 2:
                day, hours = cells[0].text, cells[1].text
                if day and hours:
                    delivery_info['hours'][day] = hours


        details_texts = ["Bazowa opłata za dostawę", "Minimalna wartość zamówienia",
                         "Maksymalna odległość bez dopłaty", "Szacowany czas dostawy"]
        for detail_text in details_texts:
            detail_value = WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((
                    By.XPATH, f"//p[contains(text(), '{detail_text}')]/span"))
            ).text.strip()
            if detail_value:
                delivery_info['details'][detail_text] = detail_value

        logging.info(f'Znaleziono informacje o dostawie dla restauracji {restaurant_url}: {delivery_info}.')
    except Exception as e:
        logging.error(f'Problem z pobraniem informacji o dostawie dla {restaurant_url}: {e}')

    return delivery_info




def scrape_wolt(base_url):
    urls = get_restaurant_urls(base_url)
    if not urls:
        logging.error('Nie znaleziono żadnych URL-i restauracji. Zakończenie działania skryptu.')
        return

    restaurants_data = {}  

    for url in urls:
        logging.debug(f'Przetwarzanie restauracji: {url}')
        restaurant_data = {}
        menu = get_menu_for_restaurant(url)
        if menu:
            restaurant_data['menu'] = menu
        address = get_address(url)
        if address:
            restaurant_data['address'] = address
        rating = get_rating(url)
        if rating:
            restaurant_data['rating'] = rating
        description = get_description(url)
        if description:
            restaurant_data['description'] = description
        delivery_info = get_delivery_info(url)
        if delivery_info:
            restaurant_data['delivery_info'] = delivery_info

        if restaurant_data:
            restaurants_data[url] = restaurant_data  

    if restaurants_data:
        file_path = 'C:\\Users\\kules\\Desktop\\scrapper\\wolt_data.json'
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(restaurants_data, f, ensure_ascii=False, indent=4)
        logging.info('Dane wszystkich restauracji zostały zapisane.')
    else:
        logging.error('Nie udało się pobrać danych dla żadnej z restauracji')

    driver.quit()

base_url = 'https://wolt.com/pl/pol/warsaw/restaurants'
scrape_wolt(base_url)


