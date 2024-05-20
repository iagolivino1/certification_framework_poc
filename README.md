
# Framework for browser certification (POC)

### Prerequisite:
Python (minimum 3.9)
___

### Install:
execute the command:
```bash
python3 -m pip install -r requirements.txt 
```

___
### Configuration:
Update the `config.yml` file with the tool you want to use and the global configuration
```
configuration:  
    platform_tool: <browserstack or saucelabs>
    lab: <lab_(same name as the yml file)> # ex: lab: qa01
  
# global credentials - optional
credentials:
    agent_0:  
        user: <five9user>
        pass: <pass>
    ...
    agent_N:
        user: <user>
        pass: <pass>

# global browser flags - optional
flags:
    <any_flag_label_1>: <browser_flag_1>
    <any_flag_label_2>: <browser_flag_2>
    ...
    <any_flag_label_N>: <browser_flag_N>
```
___
Fill the corresponding *.yml* file (that you typed in *config.yml*) inside `configuration` folder (**platform_tool** and **lab** fields).

Update the `<platform_tool>.yml` file with the browser configuration, specific flags and extensions.
Get the necessary information provided by the selected tool (ex: **saucelabs**) on its site (it is normally in the automation section).

```
# configuration section data is available on the tool website
configuration:
    hub_url: <hub_url>
    platform: Windows
    platform_version: 11
    browser: <browswer_name>-<local_or_remote>
    browser_version: <version>
    username: <tool_username>
    access_key: <tool_access_key>
    build: <tool_build>
    test_name: <any_name>

# specific browser flags (append to the global flags)
<browser_name>_flags:
    <any_flag_label_1>: <browser_flag_1>
    <any_flag_label_2>: <browser_flag_2>
    ...
    <any_flag_label_N>: <browser_flag_N>

# specific extensions (extensions file should be inside extensions/ folder)
<browser_name>_extensions:
    <any_extension_label_1>: <extension_file_name>.crx 
    ...
    <any_extension_label_N>: <extension_file_name>.crx 
```

**Note**: If you want/need to run the tests locally just fill the configuration *.yml* file with:
```
browser = chrome-local
```
___
Update the `<lab>.yml` file inside **_configuration/lab_** folder with the lab configuration and specific credentials.

```
configuration:
    login_url: <lab_url_login>
    chat_console_url: <chat_console_url>
    email_console_url: <email_console_url>
    connector_url: <connector_url>

# specific credentials (override global credentials)
credentials:
    agent_0:
        user: <user1>
        pass: <pass1>
    ...
    agent_N:
        user: <userN>
        pass: <passN>
```

___
___
### How to use:
**Go to `test/python` folder:**
```bash
cd test/python
```

**Run all scenarios:**
```bash
pytest .
```

**Run specific script:**
```bash
pytest <script_file.py>
```
example:
```bash
pytest test_check_left_menu.py
```

**Run specific scenario inside script:**
```bash
pytest <script_file.py>::<test_func>
```
example:
```bash
pytest test_check_left_menu.py::test_check_left_menu
```

**Run specific scenario by its tag:**
```bash
pytest -m "tag"
```
example:
```bash
pytest -m "check_left_menu"
```
___
___
### Steps to create new test:

1. **Create the .feature file:**\
   Using gherkin language to create a human-readable step-by-step guide that will allow anyone on the organization to 
   understand what the test is about and describing the test behaviour.
   The file must be created inside _**test/features**_ folder. \
   `my_feature.feature`:
    ```
    @feature_tag
    Feature: Your Feature
     As a test developer,
     I want to verify a specific scenario
     So I can confirm that the feature is working fine

    Background:
     Given I set the background
    
    @scenario_tag_tc_01
    Scenario: TC 01
     When I use all the necessary steps
     When I perform all the validations 
     Then I confirm that the feature is working
   
    @scenario_tag_tc_02
    Scenario: TC 02
     When I use all the other necessary steps
     When I perform all the other validations 
     Then I confirm that the feature is working
    ```
   \
.
2. **Create initialization file**:\
   It is a python file that must use the same name as the .feature file and must be created inside **_test/initialization_** 
   folder. On this case it must be `my_feature.py`. \
   Inside the initialization file must be created a function with the name of the scenario (for each existing scenario 
   inside feature file).  
   `my_feature.py`:
   ```
   from test.initialization import base_setup


   def test_case_01():
      base_setup.set_base_pages(instances=1)
      common_steps.STARTED_PAGES.append(my_feature_steps.MY_FEATURE_PAGE)
    
   def test_case_02():
      base_setup.set_base_pages(instances=2)
      common_steps.STARTED_PAGES.append(my_feature_steps.MY_FEATURE_PAGE)
      common_steps.STARTED_PAGES.append(my_other_feature_steps.MY_OTHER_FEATURE_PAGE)
   ```
   Here you must add all the pages that will be used by your scenario and also define the number of browser instances 
   you need to open in order to perform your test.\
   **Note:** The number of the instances is not always related to the number os "pages" you are appending to the STARTED_PAGES 
   variable. See some already created initialization file in case of doubt. \
.
3. **Create the pytest run file**:  
   This file is created inside of **_test/python_** folder and must contain the indication for the feature file 
   and for each scenario (that is wanted to be runnable).  
   `test_my_feature.py`:
   ```
   from pytest_bdd import scenario

   @scenario('../features/my_feature.feature', 'TC 01')
   def test_tc_01():
      pass

   @scenario('../features/my_feature.feature', 'TC 02')
   def test_tc_02():
      pass
   ```
   .  
4. **Map web elements and create page object files**:  
   On this file all the page elements that will be used in your test must be mapped.  
   A file/class must be created inside page_objects folder (chose any name).  
   No logic should be added to this file/class, it is used only for store the paths and get web elements.  
   `my_feature_page.py`:
   ```
   from selenium.webdriver.common.by import By

   class MyFeaturePage(object):
      def __init__(self, driver=None):
         self.driver = driver
         self.home_title = "//a[@id='home_title']"
         self.home_button = "//button[@id='home_button']"
      
      def get_home_title():
         return self.driver.find_element(By.XPATH, self.home_title)
      
      def get_home_button():
         return self.driver.find_element(By.XPATH, self.home_button)
   ```
   The class must be an _object_ and the constructor must always have the _driver=None_ argument.  
.
   
5. **Create step definition files**:  
   All the steps created (in the .feature file), must have its definition (automation code).\
   This file must be created inside _**step_definitions**_ folder and the only convention it follows is to keep the 
   name similar to the page object file.  
   `my_feature_page_steps.py`:
   ```
   from page_objects.home_page import HomePage
   from pytest_bdd import when, then
   
   MY_FEATURE_PAGE = MyFeaturePage()
   
   
   @when("I use all the necessary steps")
   def necessary_steps():
      assert MY_FEATURE_PAGE.get_home_title().text == 'My Feature'
   
   
   @when("I perform all the validations")
   def perform_validations():
      assert MY_FEATURE_PAGE.get_home_button().is_enabled()
      MY_FEATURE_PAGE.get_home_button().click()
   
   
   @then("I confirm that the feature is working)
   def confirm_feature():
      assert MY_FEATURE.driver.current_url == 'https://my-feature.com'
   ```