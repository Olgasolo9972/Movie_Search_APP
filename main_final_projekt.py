# Импортируем настройки из конфигурационного файла
from config import RESULTS_PAGE_SIZE

# Импортируем функции для работы с MySQL
from mysql_connector import (
    search_movies_by_keyword,
    get_all_genres,
    get_min_year,
    get_max_year,
    search_movies_by_genre_and_year_range
)

# Импорт функций для логирования поисковых запросов в MongoDB
from log_writer import log_search

# Импорт функций для получения статистики логов
from log_stats import get_last_searches, get_top_searches, close_connection

# Импорт форматирования результатов в табличную форму
from formatter import format_table


# Функция для поиска фильмов по ключевому слову
def keyword_search_flow():
    offset = 0  # Сколько фильмов уже показано (для постраничного вывода)

    while True:
        keyword = input("Enter a keyword to search in movie titles: ").strip()
        if not keyword:
            print("Keyword cannot be empty.")
            continue

        log_search("keyword", keyword)

        while True:
            results = search_movies_by_keyword(keyword, offset=offset)
            if not results:
                if offset == 0:
                    print("No movies found for your query.")
                else:
                    print("No more results.")
                break

            print(f"\nShowing results {offset + 1} to {offset + len(results)}:")
            print(format_table(results))

            if len(results) < RESULTS_PAGE_SIZE:
                print("These are the last results.")
                break

            user_input = input("Show 10 more? (yes / no): ").strip().lower()
            if user_input != 'yes':
                break

            offset += RESULTS_PAGE_SIZE
        break


# Функция для поиска фильмов по жанру и диапазону годов
def genre_year_search_flow():
    genres = get_all_genres()
    if not genres:
        print("Failed to fetch genres.")
        return

    min_year = get_min_year()
    max_year = get_max_year()

    print("Available genres:")
    for g in genres:
        print(f"- {g}")
    print(f"Year range: {min_year} - {max_year}")

    while True:
        genre = input("Enter a genre from the list above: ").strip()
        if genre.lower() not in [g.lower() for g in genres]:
            print("Invalid genre. Please try again.")
            continue
        break

    while True:
        year_from_input = input(f"Enter start year (>= {min_year}): ").strip()
        year_to_input = input(f"Enter end year (<= {max_year}): ").strip()
        try:
            year_from = int(year_from_input)
            year_to = int(year_to_input)
            if year_from < min_year or year_to > max_year or year_from > year_to:
                print("Invalid year range. Try again.")
                continue
        except ValueError:
            print("Please enter valid numbers.")
            continue
        break

    log_search("genre_year", f"{genre} {year_from}-{year_to}")

    offset = 0
    while True:
        results = search_movies_by_genre_and_year_range(genre, year_from, year_to, offset=offset)
        if not results:
            if offset == 0:
                print("No movies found for your query.")
            else:
                print("No more results.")
            break

        print(f"\nShowing results {offset + 1} to {offset + len(results)}:")
        print(format_table(results))

        if len(results) < RESULTS_PAGE_SIZE:
            print("These are the last results.")
            break

        user_input = input("Show 10 more? (yes / no): ").strip().lower()
        if user_input != 'yes':
            break

        offset += RESULTS_PAGE_SIZE


# Вывод последних 5 поисковых запросов
def show_last_searches():
    print("\nLast 5 search queries:")
    last_searches = get_last_searches(5)
    for item in last_searches:
        print(f"- {item.get('query')} (time: {item.get('timestamp')})")


# Вывод самых популярных 5 запросов
def show_top_searches():
    print("\nTop 5 search queries:")
    top_searches = get_top_searches(5)
    for item in top_searches:
        print(f"- {item.get('_id')} (count: {item.get('count')})")


# Основное меню программы
def main_menu():
    print("Welcome to the Movie Search APP!")

    while True:
        print("\nChoose an option:")
        print("1 - Search movies by keyword")
        print("2 - Search movies by genre and year range")
        print("3 - Show last 5 search queries")
        print("4 - Show top 5 search queries")
        print("0 - Exit")

        choice = input("Your choice: ").strip()

        if choice == '1':
            keyword_search_flow()
        elif choice == '2':
            genre_year_search_flow()
        elif choice == '3':
            show_last_searches()
        elif choice == '4':
            show_top_searches()
        elif choice == '0':
            print("Exiting the program. Goodbye!")
            close_connection()  # Закрываем MongoDB подключение
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
