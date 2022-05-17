from datetime import datetime
import os
import random
from selenium import webdriver
import time

from options import Options
from telegram_bot import TelegramBot

# Initialize user information and options
args = Options().parse()

# Create telegram bot
bot = TelegramBot()

# Get current time
now = datetime.now().strftime("%H:%M")

# Configure and start the webdriver
DRIVER_PATH = '/Users/Oli/Documents/Webdriver/chromedriver_mac64_m1'
#DRIVER_PATH = '/usr/lib/chromium-browser/chromedriver' #for Raspberry Pi

if args.debug:
	driver = webdriver.Chrome(executable_path=DRIVER_PATH)
else:
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)
	print("Started webdriver at {}".format(now))

# Set maximum time the driver should wait for an element to load
# before it gives up (eg. 10 seconds)
driver.implicitly_wait(10)

# Initialize flags
signed_up = False
spots_availlable = False

while not signed_up:
	for lesson_nr in args.lessonNr:
		class_link = "https://schalter.asvz.ch/tn/lessons/" + lesson_nr
		# Access the "CrossFit: Training" webpage
		driver.get(class_link)

		# Save class details
		class_details = dict()
		try:
			details_panel = driver.find_element_by_xpath("//div[@class='panel-body event-properties']")
			for detail in details_panel.find_elements_by_tag_name("dl"):
				info = detail.text.split("\n")
				class_details[info[0]] = info[1]
			
			try:
				# Check if there are any free spots available
				free_spots = int(class_details[u'Freie Pl\xe4tze'])
				if free_spots > 0:
					spots_availlable = True
					print("There is {} free spot!!".format(free_spots))
				else:
					print("There are currently {} free spots available.".format(free_spots))
			except:
				print("Failed while fetching Freie Plaetze field or parsing to int")
				print(class_details)
		except Exception as e:
			print("Event properties could not be found.")
			print(e)
			# Take a screenshot and save it in /errors 
			date_time = datetime.now()
			image_path = "errors/event_properties_not_found.png"
			print(image_path)
			driver.save_screenshot(image_path)

		# Variable to keep track of where the bot currently is.
		status = "Lesson"

		if spots_availlable:
			if not args.friend:
				# AUTO SIGN UP FOR LESSON
				try:
					# Click the login button
					driver.find_element_by_xpath("//button[@title='Login']").click()

					# Click the SwitchAai button
					status = "SwitchAai page"
					driver.find_element_by_xpath("//button[@title='SwitchAai Account Login']").click()

					# Select ETH Zuerich as institution
					status = "Select institution page"
					driver.find_element_by_xpath("//input[@id='userIdPSelection_iddtext']").send_keys("ETH")
					driver.find_element_by_xpath("//input[@type='submit']").click()

					# Enter ETH login credentials
					status = "Login page"
					driver.find_element_by_xpath("//input[@id='username']").send_keys(args.user)
					driver.find_element_by_xpath("//input[@id='password']").send_keys(args.password)
					driver.find_element_by_xpath("//button[@type='submit']").click()
					
				except NoSuchElementException:
					print("NoSuchElementException: There was a error while trying to fetch an element on page: {}.".format(status))
					break

				try:
					# Accept the forwarding of informtaion
					forward_info = driver.find_element_by_xpath("//input[@name='_eventId_proceed']")
					forward_info.click()
				except:
					print("There was no need to agree on your information being sent.")

				# Sign up for lesson
				try:
					driver.find_element_by_xpath("//button[@id='btnRegister']").click() 
				except Exception as e:
					message = bot.create_message("no_sign_up_button")
					print(message)
					print(e)
					bot.send_message(message)
					break

			# Send telegram message
			message = bot.create_message("success", class_details)
			print(message)
			telegram_message = bot.send_message(message)
			print("Telegram message was sent.")
			signed_up = True
			break

		else:
			# Try next class
			time.sleep(1)

	else:
		# Try again in approx. one minute
		print("Trying again in one minute.")
		time.sleep(random.randint(45,75))


# Close all tabs and windows after 10 seconds
time.sleep(5)
print("Stopped webdriver at {}".format(datetime.now().strftime("%H:%M")))
driver.quit()
