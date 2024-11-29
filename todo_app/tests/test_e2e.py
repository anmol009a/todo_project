from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User


class TodoE2ETestCase(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        User.objects.create_user(username="testuser", password="testpass")

    def tearDown(self):
        self.driver.quit()

    def test_todo_crud_workflow(self):
        self.driver.get(f"{self.live_server_url}/admin/")
        # Login to admin
        self.driver.find_element(By.NAME, "username").send_keys("testuser")
        self.driver.find_element(By.NAME, "password").send_keys("testpass")
        self.driver.find_element(By.XPATH, "//input[@type='submit']").click()

        # Verify login was successful
        self.assertIn("Site administration", self.driver.title)

        # Create a To-Do Item
        # (Use the admin panel or custom frontend as per the assignment)
        # Example code can be extended based on the UI
