import json

# Ścieżka do pliku źródłowego JSON
source_file_path = 'C:\\Users\\kules\\Desktop\\scrapper\\wolt_data.json'
# Ścieżka do pliku docelowego, w którym zapisany zostanie zmodyfikowany JSON
output_file_path = 'C:\\Users\\kules\\Desktop\\scrapper\\wolt_data_with_categories_prepared.json'

# Słownik zawierający mapowanie kategorii na słowa kluczowe
category_keywords = {
    'Pizza': ['Pizza', 'Pizze', 'Pizzy'],
    'Śniadanie': ['Śniadanie', 'Śniadania'],
    'Sushi': ['Sushi'],
    'Indyjska': ['Indyjskie', 'Indyjska', 'Curry'],
    'Burgery': ['Burger', 'Burgery', 'Hamburger', 'Cheeseburger'],
    'Desery': ['Lody', 'Ciasto', 'Ciasta', 'Kawa'],
    'Wegańskie': ['Vegan', 'Wegańskie', 'Wegański'],
    'Zupa': ['Zupa', 'Zupy', 'Zupka'],
    'Kawa': ['Kawa', 'Kawy'],
    'Włoska': ['Makarony', 'Makaron', 'Pizza', 'Pizze'],
    'Amerykańska': ['Hot-Dog', 'Hot Dog', 'Burger', 'Burgery'],
    'Lody': ['Lód', 'Lody'],
    'Kanapki': ['Kanapki', 'Kanapka']
}

def modify_and_categorize_restaurants(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    modified_data = {}
    for url, restaurant_info in data.items():
        # Wyodrębnienie ostatniej części URL-a jako nowy klucz
        modified_key = url.split('/')[-1]

        if 'menu' in restaurant_info:  # Sprawdzenie, czy istnieje klucz 'menu'
            menu = restaurant_info['menu']
            menu_text = json.dumps(menu)  # Przekształcenie menu na tekst
            categories = []

            # Wyszukiwanie kategorii na podstawie słów kluczowych
            for category, keywords in category_keywords.items():
                if any(keyword in menu_text for keyword in keywords):
                    categories.append(category)

            restaurant_info['categories'] = categories
        else:
            restaurant_info['categories'] = []  # Przypisanie pustej listy kategorii, jeśli 'menu' nie istnieje

        modified_data[modified_key] = restaurant_info

    return modified_data

def save_modified_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Główna logika skryptu
modified_data = modify_and_categorize_restaurants(source_file_path)
save_modified_json(modified_data, output_file_path)

print(f'Zmodyfikowany plik JSON został zapisany w pliku: {output_file_path}')
