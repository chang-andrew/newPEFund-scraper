from selenium import webdriver as web
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = web.Chrome()
driver.maximize_window()
driver.get('https://s3-us-west-1.amazonaws.com/editorial-viz/20181002-pe-first-funds-map/index.html?initialWidth=1170&childId=iframe-container&parentTitle=Where%20do%20America%27s%20new%20private%20equity%20funds%20come%20from%3F%20%7C%20PitchBook&parentUrl=https%3A%2F%2Fpitchbook.com%2Fnews%2Farticles%2Fwhere-do-americas-new-private-equity-funds-come-from')
time.sleep(20)
file = open("fundData.csv", "w")
for i in range(2003, 2019):
	file.write('\n'+str(i)+'\n')
	driver.find_element_by_id('button_'+str(i)).click()
	time.sleep(1)
	circles = driver.find_elements_by_tag_name('circle')
	for circle in circles:
		if circle.get_attribute('class') == 'legend-bubble':
			break
		try:
			circle.click()
		except:
			try:
				actions = ActionChains(driver)
				actions.move_to_element_with_offset(circle, 1, 1)
				actions.click()
				actions.perform()
			except:
				continue
		loc = driver.find_element_by_id('current-location').text
		table = driver.find_element_by_id('fund-list')
		allRows = table.find_elements_by_tag_name('tr')
		allRows.pop(0)
		for row in allRows:
			rowItems = row.find_elements_by_tag_name('td')
			lineItem = ""
			for item in rowItems:
				lineItem += item.text+','
			lineItem+=loc
			print(lineItem)
			file.write(lineItem+'\n')

