### GoIT moduł 2 web 
# Zadanie domowe #9

Wybierz bibliotekę **BeautifulSoup** lub framework **Scrapy**. Następnie wykonaj scraping strony [http://quotes.toscrape.com](http://quotes.toscrape.com). 
Twoim celem jest uzyskanie dwóch plików: `qoutes.json`, w którym należy umieścić wszystkie informacje o cytatach ze wszystkich stron witryny oraz `authors.json`, 
w którym znajdziesz informacje o autorach tych cytatów. Struktura plików json powinna być dokładnie taka sama jak w poprzednim zadaniu domowym. 
Wykonaj wcześniej napisane skrypty, aby przesłać pliki json do bazy danych w chmurze dla otrzymanych plików. 
Poprzednie zadanie domowe powinno działać poprawnie z nowo otrzymaną bazą danych.

### Zadanie dodatkowe
Do scrapingu użyj frameworka **Scrapy**. Crawler powinien zostać uruchomiony jako pojedynczy skrypt `main.py`.

> [!NOTE]
> Zadanie wykonane zarówno dla biblioteki **BeautifulSoup** (plik: `main_bs.py`), jak i przy uzyciu frameworku **Scrapy** (plik: `main_scrapy.py` oraz `main_scrapy_one_crawler.py`).
> 
> Niezbędne pliki z zadania 8, dodane do projektu w katalogu: `packages_from_homework_8` dla łatwiejszego przetestowania rozwiązania.

> [!WARNING]
> W celu poprawnego działania wysyłania danych do bazy danych,
> przed użyciem należy uzupełnić plik config.ini danymi pozwalającymi na pracę z bazą `MongoDB`
>``` 
> USER = <wpisz nazwę użytkownika>
> PASS = <wpisz hasło użytkownika>
> DB_NAME = <wpisz nazwę bazy danych>
> DOMAIN = <wpisz nazwę domeny>
>```
> lub wykomentować / usunąć poniższe fragmenty funkcji `main()`, z plików `main_bs.py`, `main_scrapy.py` i `main_scrapy_one_crawler.py`, aby nie uploadować danych do bazy:
>
> ``` Python
> print("Seeding data in database using packages from homework #8...")
> authors = load_json_data("data/authors.json")
> quotes = load_json_data("data/quotes.json")
> data_seed(authors, quotes)
> ```
> oraz wykomentować / usunąć linię:
> ``` Python
> from packages_from_homework_8.seed import load_json_data, data_seed
> ```
