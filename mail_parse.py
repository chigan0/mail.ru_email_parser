import os
from time import sleep
from threading import Thread
from typing import Union

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


url_list: dict = {"gamecandyvalley": "https://my.mail.ru/community/gamecandyvalley/friends",
		"klondike-game": "https://my.mail.ru/community/klondike-game/friends"
	}

auth_data: dict = {
	"gamecandyvalley": {"email": "dwgwgw1323", "mail": "mail.ru", "password": "gtx25122512"},
	"klondike-game": {"email": "coyah17663", "mail": "mail.ru", "password": "gtx25122512"}
}


def result_folder() -> None:
	if not os.path.exists('result'):
		os.mkdir('result')


def authorization(email: str, mail: str, password: str) -> Union[None, webdriver.Chrome]:
	if email is not None and mail is not None and password is not None:
		options = Options()
		options.headless = True
		options.add_argument("--log-level=3")
		driver = webdriver.Chrome(options=options)
		driver.get(f"https://account.mail.ru/login?&fail=1&email={email}%40{mail}")
		sleep(1.2)

		driver.find_element(By.NAME, 'password').send_keys(password)
		driver.find_element(By.CLASS_NAME, 'submit-button-wrap').click()

		return driver


def parse_settings(url, name) -> None:
	email: str = auth_data.get(name).get('email')
	mail: str = auth_data.get(name).get('mail')
	password: str = auth_data.get(name).get('password')

	browser = authorization(email, mail, password)

	page: int = 1
	thread_num: Union[None, int] = None
	page_state: bool = True
	
	if browser is not None:
		sleep(1.2)
		browser.get(f"{url}{page}")

		with open(f"result/{name}.txt", "w") as file:
			while page_state:
				page += 1
				
				soup = BeautifulSoup(browser.page_source)
				all_email: list = soup.find_all(class_="inviz")

				print(f"Page: {page}, Name: {name}")

				if len(all_email) == 0:
					page_state = False
					continue

				for user_mail in all_email:
					file.write(f"{user_mail.get_text()} \n")

				browser.get(f"{url}{page}")

				sleep(0.1)

result_folder()

for name in url_list:
	Thread(target=parse_settings, args=(f"{url_list.get(name)}?page=", name,)).start()
