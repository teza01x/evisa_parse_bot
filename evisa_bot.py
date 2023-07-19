import asyncio
import warnings
import telebot
import zipfile
from datetime import datetime, timedelta, time
from telebot.async_telebot import AsyncTeleBot
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
from sql_scripts import *
from html_elements import *
from config import *


bot = AsyncTeleBot(telegram_token)


@bot.message_handler(commands=['start'])
async def start(message):
    user_id = message.chat.id

    if not check_user_exists(user_id):
        try:
            add_user_to_db(user_id)
            await bot.send_message(user_id, "Hello, this is a notifier EVISA-bot!\n"
                                            "I send notifications about the date of the next appointments.\n"
                                            "Now you will receive the latest dates right in this chat.")
        except Exception as error:
            print(error)

    await bot.send_message(user_id, "Please stay tuned for new dates.\nAs soon as they appear - you will receive a notification in this chat.")


@bot.message_handler(commands=['launch_bot'])
async def launch_bot(message):
    user_id = message.chat.id

    if user_id == admin_id:
        try:
            if get_bot_work_status() == "True":
                await bot.send_message(user_id, "The bot is already up and running.\nWait for new information.")
            else:
                change_work_status("True")
                await bot.send_message(user_id, "🤖 You have launched the bot. 🤖")
        except Exception as error:
            print(error)
    else:
        await bot.send_message(user_id, "You do not have permission to use this command.")


@bot.message_handler(commands=['stop_bot'])
async def launch_bot(message):
    user_id = message.chat.id

    if user_id == admin_id:
        try:
            if get_bot_work_status() == "False":
                await bot.send_message(user_id, "The bot is currently disabled.\nTo launch, use the /launch_bot command")
            else:
                change_work_status("False")
                await bot.send_message(user_id, "🤖 You have stopped the bot. 🤖")
        except Exception as error:
            print(error)
    else:
        await bot.send_message(user_id, "You do not have permission to use this command.")


class General_class:
    def __init__(self, wait):
        self.wait = wait


    def wait_general_section(self, start_form):
        try:
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, start_form)))
            return True
        except:
            return False


    def choose_country(self, country):
        try:
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, country))).click()
        except Exception as error:
            print(error)


    def choose_city(self, city):
        try:
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, city))).click()
        except Exception as error:
            print(error)


    def submit_btn(self, submit):
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, submit))).click()
        except Exception as error:
            print(error)


    def make_app(self, app_form, app_btn):
        try:
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, app_form)))
        except Exception as error:
            print(error)
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, app_btn))).click()
        except Exception as error:
            print(error)


    def go_to_proc_calendar(self, proceduro_form, procedure, read_flag, submit):
        try:
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, proceduro_form)))
        except Exception as error:
            print(error)
        try:
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, procedure))).click()
        except Exception as error:
            print(error)
        try:
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, read_flag))).click()
        except Exception as error:
            print(error)
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, submit))).click()
        except Exception as error:
            print(error)


    def check_each_month_info(self, browser, calendar_form, proc):
        try:
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, calendar_form)))
        except Exception as error:
            print(error)
        try:
            proc_info = [proc]
            for month in month_dct:
                month_dates = [month]
                self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, month_dct[month]))).click()
                self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, calendar_form)))

                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')
                cells = soup.find_all('td')

                for cell in cells:
                    if cell.get('bgcolor') == '#ffffc0':
                        data = cell.text.strip()
                        if len(data) > 0:
                            data = data.replace('Available', ' Available')
                            date = data.split(' ')[0]
                            month_dates.append(date)
                if len(month_dates) > 1:
                    proc_info.append(month_dates)
            return proc_info

        except Exception as error:
            print(error)


async def get_chromedriver(proxy_ip, proxy_port, proxy_login, proxy_pass, use_proxy=False, user_agent=None):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (proxy_ip, proxy_port, proxy_login, proxy_pass)


    options = webdriver.ChromeOptions()
    options.binary_location = '/usr/bin/google-chrome'
    options.add_argument('--headless=new')
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = webdriver.chrome.service.Service(path_to_chromedriver)
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        options.add_extension(pluginfile)
    if user_agent:
        options.add_argument('--user-agent=%s' % user_agent)
    browser = webdriver.Chrome(service=service, options=options)
    return browser


async def work(browser):
    wait = WebDriverWait(browser, 30)
    browser.get(start_page_link)

    general_obj = General_class(wait)
    if general_obj.wait_general_section(html_dct['start_form']) == True:
        general_obj.choose_country(html_dct['country'])
        general_obj.choose_city(html_dct['city'])
        general_obj.submit_btn(html_dct['submit_btn'])
        general_obj.make_app(html_dct['make_app_form'], html_dct['app_btn'])

        procs_url = browser.current_url
        for proc in procs_dct:
            await asyncio.sleep(1)
            general_obj.go_to_proc_calendar(html_dct['procedure_form'], procs_dct[proc], html_dct['read_flag'],
                                            html_dct['submit_btn'])
            await asyncio.sleep(1)
            procedure_info = general_obj.check_each_month_info(browser, html_dct['calendar_form'], proc)
            await asyncio.sleep(0.5)
            if len(procedure_info) > 1:

                dates = []
                for month_dates in procedure_info[1:]:
                    dates.append("{}:\n".format(month_dates[0]) + ", ".join(month_dates[1:]))
                av_dates = "\n".join(dates)

                if get_date_info(proc) != av_dates:
                    update_date_info(proc, av_dates)


                    telegram_users = get_telegram_users()
                    for user in telegram_users:
                        if get_usr_status(user) == 0:
                            change_user_status(1, user)
                        await bot.send_message(user, "{}:\n"
                                                     "{}".format(proc, av_dates))
                elif get_date_info(proc) == av_dates:
                    telegram_users = get_telegram_users()
                    for user in telegram_users:
                        if get_usr_status(user) == 0:
                            await bot.send_message(user, "{}:\n"
                                                         "{}".format(proc, av_dates))
                            change_user_status(1, user)

            await asyncio.sleep(1.5)
            browser.get(procs_url)
    browser.quit()


async def get_data_from_website():
    if get_bot_work_status() == "True":

        with open(proxy_file, 'r') as file:
            x = file.read()

        await asyncio.sleep(0.1)

        proxy_lst = x.split('\n')
        proxy_lst = [i for i in proxy_lst if len(i) > 0]

        await asyncio.sleep(0.1)

        count = 0
        while count != len(proxy_lst):
            proxy_ip, proxy_port, proxy_login, proxy_password = proxy_lst[count].split(':')
            await asyncio.sleep(0.1)
            browser = await get_chromedriver(proxy_ip, proxy_port, proxy_login, proxy_password, use_proxy=proxy_use)
            await asyncio.sleep(0.1)

            if get_bot_work_status() == "True":
                count += 1
                browser.maximize_window()
                try:
                    await work(browser)
                except Exception as error:
                    print(error)
                await asyncio.sleep(1)
            else:
                browser.quit()
                break
            await asyncio.sleep(0.1)
    else:
        pass


async def main_processes():
    try:
        while True:
            await get_data_from_website()
            await asyncio.sleep(delay)
    except Exception as error:
        print(error)


async def main():
    bot_task = asyncio.create_task(bot.polling())
    data_mining_task = asyncio.create_task(main_processes())

    await asyncio.gather(bot_task, data_mining_task)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
