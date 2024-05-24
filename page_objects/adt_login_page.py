class ADTLoginPage(object):
    def __init__(self, driver=None):
        self.driver = driver
        self.url = "https://qaapp01d.five9lab.com/clients/integrations/adt.main.html"

    def open_page(self):
        self.driver.get(self.url)
