Wolt Scraper for Microservices
Project Overview

This project is a web scraper built with Selenium that extracts restaurant data from the Wolt platform. It is designed to automate the process of gathering restaurant information, including menus, ratings, addresses, and delivery details, from Wolt's website. The scraped data is stored in a structured JSON format for further processing or integration with a larger system, such as a microservice-based architecture for food delivery applications.

The scraper is highly modular and can be easily adapted to scrape data from other cities or platforms with similar structures.
Key Features
1. Restaurant URL Extraction

The scraper starts by navigating to a Wolt city-specific page (e.g., Warsaw) and collects URLs for individual restaurants listed on the platform. These URLs are then used as entry points for deeper scraping of restaurant-specific data.

    XPath selectors are used to find restaurant links.
    Logs are generated to track the number of URLs found.

2. Menu Scraping

For each restaurant, the scraper retrieves the available menu, including the dish names and their prices. The menu data is organized into categories (e.g., pizzas, burgers, desserts).

    Scrapes all dishes listed under each category of the menu.
    Each dish’s name and price are extracted and stored.
    Categories are mapped based on keywords like "Pizza", "Burgers", and "Sushi", making it easier to analyze.

3. Ratings Extraction

The scraper retrieves the restaurant's rating, displayed on the Wolt platform. If no rating is found or the element is missing, appropriate logs are generated to handle these exceptions.

    Extracts ratings based on CSS selectors.
    Handles cases where ratings may not be available.

4. Address and Delivery Info Collection

The scraper extracts the restaurant's address and delivery-related information. This includes delivery fees, minimum order values, and estimated delivery times, all of which are critical for food delivery applications.

    Scrapes addresses using XPath selectors.
    Extracts delivery hours and specific delivery-related details, such as the base delivery fee and minimum order amount.

5. Detailed Restaurant Description

For each restaurant, a brief description is gathered. This description typically provides insights into the restaurant’s specialty or type of cuisine.

    Description is retrieved by navigating to a detailed information section on each restaurant’s page.
    This data helps categorize restaurants further (e.g., "Italian cuisine", "Sushi specialists").

6. Error Handling and Logging

The scraper includes comprehensive error handling to ensure that issues like timeouts, missing elements, or connection problems do not crash the program. Logs are stored in scraper.log and provide detailed information on any exceptions or issues that arise during the scraping process.

    Timeouts: If a page takes too long to load, the scraper logs the issue and continues.
    NoSuchElementException: If an element like a menu or address is missing, it is logged, but the scraper proceeds with other available data.
    Cookie Banner Handling: The scraper detects and closes cookie consent banners to ensure smooth operation without manual intervention.

7. Data Storage in JSON

Once all the data is collected, it is saved in a JSON file, providing structured access to the restaurant details. This JSON file can then be used for further analysis or integrated into a larger application like a food delivery system.

    The JSON file includes details such as the restaurant’s menu, categories, ratings, and delivery information.

    Example structure:

    json

    {
      "restaurant_url": {
        "menu": {
          "Pizza Margherita": "15 PLN",
          "Cheeseburger": "20 PLN"
        },
        "rating": "4.8",
        "address": "Warsaw, Main Street 123",
        "delivery_info": {
          "hours": {
            "Monday": "10:00 AM - 10:00 PM",
            "Tuesday": "10:00 AM - 10:00 PM"
          },
          "details": {
            "Minimalna wartość zamówienia": "30 PLN",
            "Bazowa opłata za dostawę": "5 PLN"
          }
        },
        "description": "The best pizza place in Warsaw."
      }
    }

Data Processing Scripts

In addition to scraping, the project includes additional scripts to process the data and extract more meaningful insights:
1. restaurants.py

This script processes the raw scraped data by modifying the restaurant URLs and storing them in a simpler, more user-friendly format. For example, the full URL of each restaurant is reduced to just the identifier.

    Converts full URLs to a simplified form.
    Saves the modified data to a new JSON file for easier access.

2. data_preparation.py

This script analyzes the menu data and assigns categories to each restaurant based on keywords found in the menu items. Categories like "Pizza", "Sushi", and "Vegan" are automatically detected and added to the restaurant's information.

    Categorizes restaurants based on their menu.
    Generates a new JSON file with categorized data for further analysis.

3. categories.py

This script expands on data_preparation.py by assigning specific categories to restaurants based on predefined keywords. It scans each restaurant’s menu to identify which type of cuisine or food it serves.

    Keywords such as "Burger", "Sushi", and "Desserts" are used to categorize restaurants.
    A refined JSON file is created with these categories for easier filtering and searching.
