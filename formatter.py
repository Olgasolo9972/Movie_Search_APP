from tabulate import tabulate

# Справочник рейтингов MPAA
RATING_EXPLANATIONS = {
    "G": "G — General Audience (допущены все возрасты)",
    "PG": "PG — Parental Guidance Suggested (рекомендуется присутствие родителей)",
    "PG-13": "PG-13 — Parents Strongly Cautioned (до 13 лет — с родителями)",
    "R": "R — Restricted (до 17 лет — с родителями)",
    "NC-17": "NC-17 — No One 17 and Under Admitted (до 18 лет — не допускаются)",
    "NR": "NR — Not Rated (без рейтинга)"
}


def format_table(data, headers="keys"):
    """
    Форматирует список словарей в таблицу и добавляет расшифровку рейтингов.
    """
    if not data:
        return "No data to display."

    table = tabulate(data, headers=headers, tablefmt="grid", stralign="center")

    # Получим все уникальные рейтинги из данных
    used_ratings = {row['rating'] for row in data if row.get('rating')}
    legend = "\n\nRating Legend:\n" + "\n".join(
        f"{code}: {desc}" for code, desc in RATING_EXPLANATIONS.items() if code in used_ratings
    )

    return table + legend
