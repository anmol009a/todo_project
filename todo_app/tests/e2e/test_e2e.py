from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions


class AdminTodoE2ETest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up WebDriver options for Chrome
        options = ChromeOptions()
        options.headless = False  # Run in normal mode
        options.add_argument("--start-maximized")  # Start browser maximized
        # cls.driver = webdriver.Chrome(service=Service("path_to_chromedriver"), options=options)
        cls.driver = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        # Create a superuser for Django admin panel
        from django.contrib.auth.models import User

        self.admin_username = "admin"
        self.admin_password = "password"
        User.objects.create_superuser(
            username=self.admin_username,
            password=self.admin_password,
            email="admin@example.com",
        )

    def admin_login(self):
        # Login to the Django admin panel
        self.driver.get(f"{self.live_server_url}/admin/")
        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")

        username_input.send_keys(self.admin_username)
        password_input.send_keys(self.admin_password)
        password_input.send_keys(Keys.RETURN)

        # Wait for the admin dashboard to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "content-main"))
        )

    def create_todo(self):
        # Navigate to Todo section and create a new item
        self.driver.find_element(By.LINK_TEXT, "Todos").click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "ADD TODO"))
        ).click()

        self.driver.find_element(By.NAME, "title").send_keys("Test Todo")
        self.driver.find_element(By.NAME, "description").send_keys(
            "E2E Testing for Todo"
        )
        self.driver.find_element(By.NAME, "status").send_keys("OPEN")
        self.driver.find_element(By.NAME, "due_date").send_keys("2024-12-30")
        self.driver.find_element(By.NAME, "_save").click()

        # Assert creation success
        success_message = (
            WebDriverWait(self.driver, 10)
            .until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".messagelist .success")
                )
            )
            .text
        )
        self.assertIn("was added successfully.", success_message)

    def update_todo(self):
        # Update the Todo item
        self.driver.find_element(By.LINK_TEXT, "Test Todo").click()
        title_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "title"))
        )
        title_field.clear()
        title_field.send_keys("Updated Todo")
        self.driver.find_element(By.NAME, "_save").click()

        # Assert update success
        success_message = (
            WebDriverWait(self.driver, 10)
            .until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".messagelist .success")
                )
            )
            .text
        )
        self.assertIn("was changed successfully.", success_message)

    def delete_todo(self):
        # Delete the Todo item
        self.driver.find_element(By.LINK_TEXT, "Updated Todo").click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Delete"))
        ).click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit']"))
        ).click()

        # Assert deletion success
        success_message = (
            WebDriverWait(self.driver, 10)
            .until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".messagelist .success")
                )
            )
            .text
        )
        self.assertIn("was deleted successfully.", success_message)

    def test_crud_operations(self):
        # Perform CRUD operations in sequence
        self.admin_login()
        self.create_todo()
        self.update_todo()
        self.delete_todo()
