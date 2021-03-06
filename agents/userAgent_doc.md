UserAgent Python API Documentation
- Dependencies
  - Selenium Web Driver
  - BS4 Beautiful Soup
  - Randint from numpy.py
  - Sample from random.py
  - Time
- Class UserAgent
  - Terms
    - These terms are used to randomize the google search queue in the API. Users may change these around as they see fit. 
  - __init__
    - Initializes options as the Options variable we imported from selenium webdrivers “firefox” options
    - Adds headless command, bypassing the browser physically opening
    - Initializes firefox as our browser of choice and allows the API to be ready to take more commands
  - store_page()
    - Formats page information
  - Google_Query()
    - API takes the query parameter and googles it. 
  - get_page()
     - API travels to the url, stores it, and prints the first 300 bytes.
  - close_browser()
     - Closes and quits API
  - random_query()
    - API Randomly chooses words from our pre-made list
    - Prints out the new query, then travels to that destination
  - get_urls_in_page()
    - API Finds all links and puts them into an array, then prints them one by one
  - random_click()
    - API Picks a random link from query and simulates a click
