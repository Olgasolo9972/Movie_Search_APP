import pymysql
from config import MYSQL_CONFIG, RESULTS_PAGE_SIZE


def get_connection():
    return pymysql.connect(
        host=MYSQL_CONFIG["host"],
        user=MYSQL_CONFIG["user"],
        password=MYSQL_CONFIG["password"],
        database=MYSQL_CONFIG["database"],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


def search_movies_by_keyword(keyword: str, offset: int = 0):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                query = """
                    SELECT title, description, release_year, rating
                    FROM film
                    WHERE title LIKE %s
                    LIMIT %s OFFSET %s;
                """
                cursor.execute(query, (f"%{keyword}%", RESULTS_PAGE_SIZE, offset))
                return cursor.fetchall()
    except pymysql.MySQLError as err:
        print(f"MySQL error: {err}")
        return []


def get_all_genres():
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                query = "SELECT name FROM category ORDER BY name;"
                cursor.execute(query)
                return [row["name"] for row in cursor.fetchall()]
    except pymysql.MySQLError as err:
        print(f"MySQL error while getting genres: {err}")
        return []


def get_year_range():
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                query = "SELECT MIN(release_year) AS min_year, MAX(release_year) AS max_year FROM film;"
                cursor.execute(query)
                result = cursor.fetchone()
                return result["min_year"], result["max_year"]
    except pymysql.MySQLError as err:
        print(f"MySQL error while getting year range: {err}")
        return (2000, 2025)


def get_min_year():
    return get_year_range()[0]


def get_max_year():
    return get_year_range()[1]


def search_movies_by_genre_and_year_range(genre: str, year_from: int, year_to: int, offset: int = 0):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                query = """
                    SELECT f.title, f.description, f.release_year, f.rating
                    FROM film f
                    JOIN film_category fc ON f.film_id = fc.film_id
                    JOIN category c ON fc.category_id = c.category_id
                    WHERE LOWER(c.name) = LOWER(%s)
                      AND f.release_year BETWEEN %s AND %s
                    LIMIT %s OFFSET %s;
                """
                cursor.execute(query, (genre, year_from, year_to, RESULTS_PAGE_SIZE, offset))
                return cursor.fetchall()
    except pymysql.MySQLError as err:
        print(f"MySQL error during genre-year search: {err}")
        return []
