from queue import Queue
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time

class GoogleCalendarAutomation:


    def __init__(self):
        options = webdriver.ChromeOptions()

        options.add_argument(
            "--user-data-dir=/Users/brunomaximo/Documents/CS/selenium-chrome-profile"
        )
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)


    def create_event(self, event_queue: Queue):
        # obs: isso poderia ser feito mil vezes mais rapido só usando o API do google calendar
        # mas o propósito aqui é praticar selenium



        driver = self.driver
        wait = self.wait

        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
                """
            }
        )


        try:

            driver.get("https://calendar.google.com")


            create_button = wait.until(
                ec.element_to_be_clickable(
                    (By.XPATH, "//button[.//span[normalize-space()='Create']]"))
            )
            create_button.click()




            event_option = self.wait.until(
                ec.element_to_be_clickable((By.XPATH, "//li[@role='menuitem' and normalize-space()='Event']")
            ))

            event_option.click()
            # time.sleep(1)

            print("Estruturando dados...")
            event = event_queue.get()


            if event is None:
                print("✗ Falha ao extrair evento")

                return

            if not event.is_event:
                print(f"\033[31m✗ Conteúdo inválido: {event.description}\033[0m")

                return

            print("\033[32m✓ Schema mapeado.\033[0m")
            print("\n[3/4] Preenchendo formulario...")


            print(f"Preenchendo nome: {event.name}")
            title_input = wait.until(
                ec.presence_of_element_located(
                    (By.XPATH, "//input[@aria-label='Add title']"))
            )
            title_input.clear()
            title_input.send_keys(event.name)


            print(f"Preenchendo data: {event.date}")
            date_input = wait.until(
                ec.presence_of_element_located(
                    (By.XPATH, "//span[@data-key='startDate']")
                )
            )
            date_input.click()
            time.sleep(0.3)
            active = driver.switch_to.active_element
            active.send_keys(Keys.COMMAND, "a")
            active.send_keys(Keys.BACKSPACE)
            active.send_keys(event.date)
            time.sleep(0.1)
            active.send_keys(Keys.TAB)





            active = driver.switch_to.active_element

            if event.start_time:
                active.send_keys(event.start_time)
                if not event.start_time == "11:11":
                    print(f"Preenchendo horario de inicio: {event.start_time}")

            active.send_keys(Keys.TAB)

            active = driver.switch_to.active_element

            if event.end_time:
                active.send_keys(event.end_time, Keys.TAB)
                if not event.end_time == "11:11":
                    print(f"Preenchendo horario de fim: {event.end_time}")

            active.send_keys(Keys.TAB)
            if event.all_day:
                active = driver.switch_to.active_element
                active.click()
                time.sleep(1)
                active = driver.switch_to.active_element
                active.click()
                active.send_keys(Keys.TAB)
                active = driver.switch_to.active_element
                time.sleep(0.1)
                if event.end_date:
                    active.send_keys(event.end_date)
                    print(f"Preenchendo data de fim: {event.end_date}")




            if event.location:
                print(f"Preenchendo localização: {event.location}")
                try:
                    location_wrapper = wait.until(
                        ec.element_to_be_clickable(
                            (By.XPATH, "//span[@data-key='location']")
                        )
                    )
                    time.sleep(0.5)
                    location_wrapper.click()
                    time.sleep(0.5)
                    active = driver.switch_to.active_element
                    active.send_keys(event.location)

                except Exception as e:
                    print(f"Aviso: Não foi possível adicionar localização: {e}")


            if event.description:
                print(f"Preenchendo descrição: {event.description}")
                try:
                    description_wrapper = wait.until(
                        ec.element_to_be_clickable(
                            (By.XPATH, "//span[@data-key='description']")
                        )
                    )
                    time.sleep(0.5)
                    description_wrapper.click()
                    time.sleep(0.5)
                    active = driver.switch_to.active_element
                    active.send_keys(event.description)

                except Exception as e:
                    print(f"Aviso: Não foi possível adicionar descrição: {e}")


            print("Salvando evento...")
            save_button = wait.until(
                ec.element_to_be_clickable((By.XPATH, "//button[contains(., 'Save')]"))
            )
            save_button.click()



            print("\n[4/4] Confirmando criação do evento...")
            time.sleep(0.5)
            try:

                wait.until(
                    ec.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{event.name[:20]}')]"))
                )
                print("\033[32m✓ Evento criado com sucesso.\n\033[0m")
                return True
            except:
                print("\033[33m! Evento provavelmente criado (timeout na verificação)\033[0m")
                return True

        except Exception as e:
            print(f"✗ Erro ao criar evento: {e}")
            return False
        finally:
            if driver:
                driver.quit()