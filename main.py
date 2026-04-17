import sqlite3
import Levenshtein 

def search_improved(conn, query, max_distance=2):
    cursor = conn.cursor()
    query_lower = query.lower().strip()
    
    # Извлекаем все названия из БД
    cursor.execute("SELECT name FROM products")
    all_names = [row[0] for row in cursor.fetchall()]
    
    exact_matches = []
    partial_matches = []
    similar_matches = []
    
    for name in all_names:
        name_lower = name.lower()
        
        # 1. Точные совпадения
        if name_lower == query_lower:
            exact_matches.append(name)
            continue
            
        # 2. Частичные совпадения (вхождение подстроки)
        if query_lower in name_lower:
            partial_matches.append(name)
            continue
            
        # 3. Поиск похожих названий (по расстоянию Левенштейна)
        # Разбиваем название на слова, чтобы искать опечатки в конкретных словах товара
        words = name_lower.split()
        if words:
            # Ищем минимальное расстояние среди всех слов в названии
            min_dist = min(Levenshtein.distance(query_lower, word) for word in words)
            
            # Если опечатка незначительная (<= max_distance), добавляем в похожие
            if min_dist <= max_distance:
                similar_matches.append(name)
                
    return exact_matches, partial_matches, similar_matches

# Функция для вывода
def print_results(exact, partial, similar):
    print(f" Результаты поиска:\n")
    
    if exact:
        print(" Точные совпадения:")
        for item in exact:
            print(f"  - {item}")
            
    if partial:
        print("\n Частичные совпадения:")
        for item in partial:
            print(f"  - {item}")
            
    if similar:
        print("\n Возможно, вы искали:")
        for item in similar:
            print(f"  - {item}")
            
    if not exact and not partial and not similar:
        print(" Совпадений не найдено.\n")
