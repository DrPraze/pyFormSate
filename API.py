from flask import Flask
from flask_restful import Api, Resource
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.firefox import GeckoDriverManager
import time, os, urllib
from bs4 import BeautifulSoup

app = Flask(__name__)
api = Api(app)

class GetFields(Resource):
	def get(self, url):
		try:
			readsite = urllib.request.urlopen(url).read()
			soup = BeautifulSoup(readsite)
			list_of_input_names = [link.get('name') for link in soup.find_all('input')]
			submit_btns = [link.get('name') for link in soup.find_all('submit')]

			return {"Success": True,
				"Url":url,
				"values":str(list_of_input_names),
				"submit":str(submit_btns)
			}
		except Exception as e:
			return {"Success": False, "Url":url, "Error":e}


class AutoFill(Resource):
	def get(self, elements, values, submit, url):
		# browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())	#for Firefox user
		# browser = webdriver.Safari()	#uncomment this for macOS users[for others use chrome via chromedriver]
		browser = webdriver.Chrome()	#for chrome users
		browser.get((url))
		list_of_input_names = eval(elements)
		submit_btns = eval(submit)
		try:
			for i in list_of_input_names:
				for j in values:
					n = browser.find_element_by_name(i)
					n.send_keys(j)
			# The next line below gets only the first submit button in a case where
			# there are several submit buttons in the site
			submit_btn = browser.find_element_by_name(submit_btns[0])
			submit_btn.click()
			#=== To quit the browser uncomment the following lines ===
			# time.sleep(3)
			# browser.quit()
			# time.sleep(1)
			# browserExe = "Safari"
			# os.system("pkill "+browserExe)

			return {"Success": True, "Url":link}
		except Exception as e:
			print("An error occured", e)

			#=== To quit the browser, uncomment the following lines ===
			# browser.quit()
			# browserEXE = "Safari"
			# os.system("pkill "+browserExe)
			return {"Success": False, "Url":link}		


api.add_resource(GetFields, "/getfields/<path:url>")

api.add_resource(AutoFill, "/autofill/<string:elements>/<string:values>/<string:submit>/<path:url>")

if __name__== '__main__':
	app.run(debug=True)
