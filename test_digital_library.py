## Import libraries
import pytest
import pandas as pd
import requests
from io import StringIO
from digital_library import Book, Library

## Read in data (this code reads data directly from GitHub)
url = 'https://github.com/esnt/Data/raw/main/CleanData/library_books.csv'
response = requests.get(url)
response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
data = pd.read_csv(StringIO(response.text))
# data = pd.read_csv(url)

# book = Book('1310', 'NewBook', 'NewAuthor', 'Mystery', 270, 2010)

@pytest.fixture
def library():
    return Library(data)

@pytest.fixture
def example_book():
    return Book('1310', 'NewBook', 'NewAuthor', 'Mystery', 270, 2010)


def test_book(example_book):
    assert example_book.get_age() == 14  # Adjust according to the current year
    assert example_book.is_long() is False
    expected_summary = 'Book ID 1310: NewBook by NewAuthor has 270 pages. It was first published in 2010 and belongs to the Mystery genre.'
    assert example_book.summary() == expected_summary

def test_library(library, example_book):
    library = Library(data)
    assert library.size == 1310
    assert library.authors == 534

    library.add_book(example_book)
    assert example_book.book_id in library.data['book_id'].values

    library.remove_book(example_book.book_id)
    assert example_book.book_id not in library.data['book_id'].values

    auth = library.get_books_by_author("Shel Silverstein")
    assert isinstance(auth, pd.DataFrame)

    gen = library.get_genre_count()
    assert isinstance(gen, pd.Series)

def test_add_book(library, example_book):
    library.add_book(example_book)
    assert example_book.book_id in library.data['book_id'].values
    assert library.size == 1311
    assert library.authors == 535

def test_remove_book(library, example_book):
    library.add_book(example_book)
    library.remove_book(example_book.book_id)
    assert example_book.book_id not in library.data['book_id'].values
    assert library.size == 1310
    assert library.authors == 534

def test_get_books_by_author(library):
    expected_books = [
        {'book_id': 5, 'title': 'The Giving Tree', 'author': 'Shel Silverstein', 'genre': 'Childrens', 'pages': 64, 'published_year': 1964},
        {'book_id': 26, 'title': 'A Light in the Attic', 'author': 'Shel Silverstein', 'genre': 'Poetry', 'pages': 176, 'published_year': 1981},
        {'book_id': 98, 'title': 'Where the Sidewalk Ends', 'author': 'Shel Silverstein', 'genre': 'Poetry', 'pages': 176, 'published_year': 1974},
        {'book_id': 118, 'title': 'Falling Up', 'author': 'Shel Silverstein', 'genre': 'Poetry', 'pages': 178, 'published_year': 1996},
        {'book_id': 271, 'title': 'The Missing Piece', 'author': 'Shel Silverstein', 'genre': 'Poetry', 'pages': 112, 'published_year': 1976},
        {'book_id': 294, 'title': 'The Missing Piece Meets the Big O', 'author': 'Shel Silverstein', 'genre': 'Childrens', 'pages': 104, 'published_year': 1981},
        {'book_id': 412, 'title': 'Runny Babbit: A Billy Sook', 'author': 'Shel Silverstein', 'genre': 'Poetry', 'pages': 96, 'published_year': 2005},
        {'book_id': 1284, 'title': 'Lafcadio, the Lion Who Shot Back', 'author': 'Shel Silverstein', 'genre': 'Childrens', 'pages': 112, 'published_year': 1963},
        {'book_id': 1289, 'title': "Uncle Shelby's ABZ Book", 'author': 'Shel Silverstein', 'genre': 'Humor', 'pages': 80, 'published_year': 1961},
        {'book_id': 1292, 'title': 'Hamlet as Told on the Street', 'author': 'Shel Silverstein', 'genre': 'Poetry', 'pages': 18, 'published_year': 1998}
    ]
    result = library.get_books_by_author("Shel Silverstein")
    
    for expected in expected_books:
        assert any(result['book_id'].values == expected['book_id']) # Check if the result matches expected books

def test_get_genre_count(library):
    genre_counts = library.get_genre_count()
    expected_genre_counts = {
        'Fiction': 235,
        'Fantasy': 211,
        'Young Adult': 103,
        'Romance': 90,
        'Nonfiction': 88,
        'Historical Fiction': 61,
        'Science Fiction': 57,
        'Mystery': 41,
        'History': 36,
        'Classics': 30,
        'Graphic Novels': 30,
        'Paranormal Romance': 23,
        'Science': 23,
        'Poetry': 19,
        'Paranormal': 17,
        'Psychology': 16,
        'Short Stories': 16,
        'Biography': 15,
        'Comics': 13,
        'Picture Books': 12,
        'Thriller': 12,
        'Childrens': 12,
        'Urban Fantasy': 11,
        'Memoir': 11,
        'New Adult': 11,
        'M M Romance': 10,
        'Horror': 10,
        'Self Help': 10,
        'Christian': 10,
        'Urban': 9,
        'Star Wars': 8,
        'Christian Fiction': 8,
        'Vampires': 8,
        'Philosophy': 7,
        'Spirituality': 7,
        'Music': 6,
        'Business': 6,
        'Steampunk': 6,
        'Humor': 6,
        'Religion': 6
    }
    
    for genre, count in expected_genre_counts.items():
        assert genre_counts[genre] == count

def test_get_book_summary(library):
    summary = library.get_book_summary('1285')
    expected = 'Book ID 1285: Blue Fire by Janice Hardy has 373 pages. It was first published in 2010 and belongs to the Fantasy genre.'
    assert expected == summary
