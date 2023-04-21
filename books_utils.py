""" 
books_utils handles multiple book related classes and functions,  
we can use them to load and update books info, search rate and comment 
a book.

Classes included: Book, BookList, BookShelf
Functions included: load_books, save_books

NAME: Tianzi Qin
SEMESTER: Spring 23
"""
import pandas as pd 
import json
from typing import List


class Book:
    """A book class contains the following properties:

    Attributes: 
        id (int) - an unique book id
        name (str) - a name for the book
        author (str) - author for the book  
        rating (float) - the rating for the book rated by users 
        reviews (int) - the number of reviews 
        genre (str) - book genre Fiction / Non Fiction 
        intro (str) - An introduction for the book 
        comments (str) - detailed comments for the book, a json string format,  
                         used as dictionary, {'user name': 'rate comment'}
    """

    def __init__(self, id: int, name: str, author: str,
                 rating: float, reviews: int, genre: str,
                 intro: str = '', comments: str = '{}'):
        """ Constructor of the Book object. """
        self.id = id
        self.name = name
        self.author = author
        self.rating = rating
        self.reviews = reviews
        self.genre = genre
        self.intro = intro  
        self.comments = json.loads(comments)

    @property
    def score(self) -> float: 
        """ Returns a score of the book which is used for book recommend """
        return 0.7 * self.rating + 0.3 * self.reviews

    def change_rating(self, rate: int) -> None: 
        """ When a user rates, increase the number of reviews and change 
            the overall rating  

        Args:
            rate (int): user rate 
        """        
        total_rating = self.rating * self.reviews
        self.reviews += 1
        self.rating = round((total_rating + rate)/self.reviews, 1)

    def add_comment(self, user: str = "", rate: str = "", comment: str = "") -> None:   
        """ When a user comments, add value to the comments: {'user name': 'rate comment'} 

        Args:
            user (str): user name 
            rate (str): user rate 
            comment (str): user comment
        """    
        self.comments[user] = rate + " " + comment

    def __str__(self) -> str:
        """ Returns a nicely formatted string of the book with name, author, rating, 
        and reviews """
        string = f"Id: {self.id} Name: {self.name}\nAuthor: {self.author}\nRating: {self.rating}  Reviews: {self.reviews}"
        return string 
    

class BookList:
    """ The BookList class is a collection of Book objects. It has the following properties:

    Attributes: 
        books (List[Book]): A list of book objects 
    """

    def __init__(self, books: List[Book]):
        """ Constructor of the BookList object. """
        self.books = books 
    
    def top_books(self, genre: str, rank: int = 10) -> List[Book]:  
        """ Return a recommend list of top 10 books in different genres, 
        rank books by scores  
        
        Args:  
            genre (str): Fiction/Non Fiction 
            rank (int): top X books, defaults to top 10 
            
        Return: 
             board (List[Book]): A list of book objects 
        """
        books_genre = [book for book in self.books if book.genre.lower() == genre.lower()] 
        board = sorted(books_genre, key = lambda book: book.score, reverse=True)[: rank] 
        return board    

    def find_by_id(self, id: str) -> List[Book]:
        """ Search books by id 
        
        Args:  
            id (int): unique book id 
            
        Return: 
             result (List[Book]): A list of book objects 
        """
        result = []
        for book in self.books: 
            if book.id == int(id): 
                result.append(book) 
        return result 
    
    def find_by_name(self, short_name: str) -> List[Book]:   
        """ Search books by short name 
        
        Args:  
            short name (str): short name of books
            
        Return: 
             result (List[Book]): A list of book objects 
        """    
        result = [] 
        for book in self.books: 
            if short_name.lower() in book.name.lower(): 
                result.append(book) 
        return result  
    
    def find_by_author(self, author: str) -> List[Book]:   
        """ Search books by author name 
        
        Args:  
            author (str): short author name of books
            
        Return: 
             result (List[Book]): A list of book objects 
        """  
        result = [] 
        for book in self.books: 
            if author.lower() in book.author.lower(): 
                result.append(book) 
        return result 


class BookShelf:  
    """ The BookShelf class is a collection of Book objects. It has the following properties:

    Attributes: 
        name (str): The name of the bookshelf, usually user's name 
        collects (dict): An empty dict, save books users add to the bookshelf, 
                         format: {book id: book name} 
    """
    def __init__(self, name):   
        """ Constructor of the BookShelf object. 
        
        Args: 
            name (str): The name of the bookshelf, usually user's name 
        """ 
        self.name = name
        self.collects = {}
    
    def add_collect(self, book: Book) -> None:   
        """ Add books to the bookshelf 
        
        Args: 
           book (Book): books users add 
        """
        id = book.id
        self.collects[id] = book.name 
    

def load_books(filename: str) -> BookList:
    """  Read the file specified by filename, and return a BookList object.  

    Args: 
        filename (str): an excel file name
    """
    df = pd.read_excel(filename)  
    comments = [comment.replace("'", '"') for comment in df.comments] 
    df.comments = comments
    data = []
    for index, row in df.iterrows():
        # create a Book instance with data from the row
        book = Book(row['id'], row['name'], row['author'],
                    row['rating'], row['reviews'], row['genre'],
                    row['intro'], row['comments'])
        # add the Book instance to the list
        data.append(book) 
    return BookList(data)   


def save_books(filename: str, books_list: BookList) -> None:
    """  Read the file specified by filename, and return a TodoList object.  

    Args: 
        filename (str): an excel file name
    """ 
    df = pd.DataFrame([vars(book) for book in books_list.books]) 
    df.to_excel(filename, index = False)     
    
    








