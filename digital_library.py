## Import necessary libraries
import pandas as pd
from datetime import datetime as dt
from typing import Any


## Book Class
class Book:
    """
    Doctests: python3 -m doctest digital_library.py
    >>> book = Book('100', 'NewBook', 'NewAuthor', 'Mystery', 270, 2010)
    >>> book.get_age()   # in 2024
    14
    >>> book.is_long()
    False
    >>> book.summary()
    'Book ID 100: NewBook by NewAuthor has 270 pages. It was first published in 2010 and belongs to the Mystery genre.'
    """
    def __init__(self, book_id: str, title: str, author:str, genre: str, pages: int, published_year: int):
        self.book_id = book_id  # Unique identifier for each book (string)
        self.title = title  # Title of the book
        self.author = author  # Author of the book
        self.genre = genre  # Genre of the book (e.g. Fiction, Non-Fiction, Mystery, Sci-Fi)
        self.pages = pages  # Number of pages in the book
        self.published_year = published_year  # The year the book was published.

    def get_age(self) -> int:
        return dt.now().year - self.published_year
    
    def is_long(self) -> bool:
        return self.pages > 300
        
    def summary(self) -> str:
        return f"Book ID {self.book_id}: {self.title} by {self.author} has {self.pages} pages. It was first published in {self.published_year} and belongs to the {self.genre} genre."

    def __str__(self):  # added for my sake
        return f"{self.title} by {self.author} ({self.published_year})"

    def __repr__(self):  # added for my sake
        return f"Book({self.book_id}, '{self.title}', '{self.author}', 'Genre: {self.genre}', {self.pages} pages, {self.published_year})"
    
class Library:
    """
    Doctests: python3 -m doctest digital_library.py
    >>> df = pd.read_csv('library_books.csv')
    >>> library = Library(df)
    >>> library.size
    1310
    >>> library.authors
    534
    >>> book = Book('1310', 'NewBook', 'NewAuthor', 'Mystery', 270, 2010)
    >>> library.add_book(book)
    >>> book.book_id in library.data['book_id'].values
    True
    >>> library.size
    1311
    >>> library.authors
    535
    >>> library.remove_book(book.book_id)
    >>> book.book_id in library.data['book_id'].values
    False
    >>> library.size
    1310
    >>> library.authors
    534
    >>> library.get_book_summary('1285')
    'Book ID 1285: Blue Fire by Janice Hardy has 373 pages. It was first published in 2010 and belongs to the Fantasy genre.'
    """
    def __init__(self, data: pd.DataFrame):
        self.data = data  # A pandas DataFrame loaded from the provided CSV file.
        self.size = data.shape[0]  # Number of books in the library.
        self.authors = data['author'].nunique()  # Number of unique authors in the library.

    def add_book(self, book: Book):
        """
        Takes an instance of Book and adds it to the DataFrame.
        All Library attributes should be updated accordingly.
        If the book already exists in library the method should
        return "Error: book_id {book_id} is already in the library."
        """
        if book.book_id in self.data['book_id'].values:
            return f"Error: book_id {book.book_id} is already in the library."
        else:
            new_book = {'book_id': book.book_id, 'title': book.title, 'author': book.author,
            'genre': book.genre, 'pages': book.pages, 'published_year': book.published_year}
            self.data = self.data._append(new_book, ignore_index=True)
            self.size = self.data.shape[0]
            self.authors = self.data['author'].nunique()

    def remove_book(self, book_id: str):
        """
        Takes a {book_id} and removes the corresponding book 
        from the DataFrame. All Library attributes should be 
        updated accordingly. If the book_id is not in the 
        library, the method should return the string: 
        "Error: {book_id} is not in the library."
        """
        if book_id not in self.data['book_id'].values:
            return f"Error: {book_id} is not in the library."
        else:
            idx = self.data[self.data['book_id'] == book_id].index
            self.data = self.data.drop(idx)
            # self.data = self.data[self.data['book_id'] != book_id]  # alt method to Remove the book using boolean indexing
            self.size = self.data.shape[0]
            self.authors = self.data['author'].nunique()

    def get_books_by_author(self, author: str):
        """
        Takes an author's name and returns a DataFrame containing 
        all books by that author. If author is not in the library, 
        the method should return the string: "No books by author 
        in library"
        """
        if author not in self.data['author'].values:
            return f"No books by {author} in library"
        else:
            return self.data[self.data['author'] == author]

    def get_genre_count(self) -> pd.Series:
        """
        Return a series with the count of books in each genre.
        """
        return self.data['genre'].value_counts()
    
    def get_book_summary(self, book_id: str) -> str:
        """
        Takes a {book_id} and returns a string with the format:
        "Book ID {book_id}: title by author has {pages} pages. 
        It was first published in {published_year} and belongs 
        to the {genre} genre."
        If the book_id is not in the library, it should return 
        "No matching book in the library."
        """
        if str(book_id) not in self.data['book_id'].astype(str).values:
            return f"No matching book in the library."
        else:
            book = self.data[self.data['book_id'].astype(str) == str(book_id)].iloc[0]
            return (f"Book ID {book['book_id']}: {book['title']} by {book['author'].strip()} has {book['pages']} pages."
                    f" It was first published in {book['published_year']} and belongs to the {book.genre} genre.")

    def __str__(self):
        """
        Should return a string representing the library. When 
        a Library object is printed, the string "There are {size} 
        books in the library by {authors} unique authors. The 
        oldest book in the library is {title} by {author} published 
        in {published_year}." should be output.
        """
        oldest = 2024
        id = 0
        for index, row in self.data.iterrows():
            book_id = row['book_id']
            year = row['published_year']
            if year < oldest:
                oldest = year
                id = book_id
        old_book = self.data[self.data['book_id'] == id].iloc[0]
        return (f"There are {self.size} books in the library by {self.authors} unique authors. The "
        f"oldest book in the library is {old_book['title']} by {old_book['author']} published "
        f"in {old_book['published_year']}.")

