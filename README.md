
# Framework for browser certification (POC)

### Prerequisite:
Python (minimum 3.9)

### Install:
execute the command:
```bash
python3 -m pip install -r requirements.txt 
```

### Configuration:
Update the `config.ini` file with the tool you want to use and a valid user
```
[configuration]  
platform_tool = <browserstack or saucelabs>
  
[credentials]  
user = <five9user>
pass = <pass>
```

Update the corresponding *.ini* file (that you updated in *config.ini*) inside `configuration` folder.
Get the necessary information provided by the selected tool on its site (it is normally in the automation section).

**Note**: If you want/need to run the tests locally just update the configuration *.ini* file with:
```
browser = chrome-local
```


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
