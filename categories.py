import json
import os

# Ścieżka do pliku źródłowego
input_file_path = 'C:\\Users\\kules\\Desktop\\scrapper\\wolt_data.json'
# Ścieżka do pliku wynikowego
output_file_path = 'C:\\Users\\kules\\Desktop\\scrapper\\wolt_data_with_categories.json'

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

# Wczytanie danych z pliku
with open(input_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Przetwarzanie każdej restauracji
for url, restaurant_info in data.items():
    if 'menu' in restaurant_info:  # Sprawdzenie, czy informacje o restauracji zawierają klucz 'menu'
        menu = restaurant_info['menu']
        menu_text = json.dumps(menu)  # Przekształcenie menu na tekst, aby ułatwić wyszukiwanie słów kluczowych
        categories = []

        # Wyszukiwanie kategorii na podstawie słów kluczowych
        for category, keywords in category_keywords.items():
            if any(keyword in menu_text for keyword in keywords):
                categories.append(category)

        # Dodanie znalezionych kategorii do informacji o restauracji
        restaurant_info['categories'] = categories
    else:
        # Jeśli 'menu' nie istnieje, przypisz pustą listę kategorii
        restaurant_info['categories'] = []

# Zapisanie zmodyfikowanych danych do nowego pliku JSON
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f'Dane zostały zapisane w {output_file_path}')
