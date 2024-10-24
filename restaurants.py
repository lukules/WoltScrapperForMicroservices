import json

# Ścieżka do pliku źródłowego JSON
source_file_path = 'C:\\Users\\kules\\Desktop\\scrapper\\wolt_data.json'
# Ścieżka do pliku docelowego, w którym zapisany zostanie zmodyfikowany JSON
output_file_path = 'C:\\Users\\kules\\Desktop\\scrapper\\modified_wolt_data.json'

def modify_restaurant_urls_in_json(file_path):
    """
    Funkcja czyta plik JSON, modyfikuje klucze (URL-i restauracji) przez wyodrębnienie ostatniej części URL-a, i zwraca zmodyfikowany słownik.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    modified_data = {}
    for url in data.keys():
        # Wyodrębnienie ostatniej części URL-a jako nowy klucz
        modified_key = url.split('/')[-1]
        modified_data[modified_key] = data[url]

    return modified_data

def save_modified_json(data, file_path):
    """
    Funkcja zapisuje zmodyfikowane dane do pliku JSON.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Główna logika skryptu
modified_data = modify_restaurant_urls_in_json(source_file_path)
save_modified_json(modified_data, output_file_path)

print(f'Zmodyfikowany plik JSON został zapisany w pliku: {output_file_path}')
