import sqlite3
import difflib
def search_original(conn, query):
    cursor = conn.cursor()
    
    # Приводим запрос к нижнему регистру
    query_lower = query.lower().strip()
    
    # Извлекаем все названия из БД
    cursor.execute("SELECT name FROM products")
    all_names = [row[0] for row in cursor.fetchall()]
    
    exact_matches = []
    partial_matches = []
    
    for name in all_names:
        # Приводим название из БД к нижнему регистру
        name_lower = name.lower()
        
        # Разделяем на точные и частичные совпадения
        if name_lower == query_lower:
            exact_matches.append(name)
        elif query_lower in name_lower:
            partial_matches.append(name)
            
    return exact_matches, partial_matches

# Функция для красивого вывода
def print_results(exact, partial):
    if not exact and not partial:
        print("❌ Совпадений не найдено.\n")
        return
