""" 
This is the main view for the application. It is responsible for
displaying the information to the client, and getting input from the client. 

NAME: Tianzi Qin
SEMESTER: Spring 23
"""
from typing import List, Tuple, Union
import books_utils
import users_utils
from enum import Enum
import sys


class Menu(Enum):
    """ The options for the menu """
    SEARCH = 1
    RECOMMEND = 2
    BOOKSHELF = 3
    HELP = 4
    EXIT = 5
    UNKNOWN = 6


def print_welcome() -> None:
    """ Print the welcome message """
    print('Welcome to Find Your Book!')
    print()


def print_help() -> None: 
    """ Print the help message """
    print('Type "help" to get a list of commands.')
    print()


def print_goodbye() -> None:
    """ Print the exit message """
    print('Enjoy your reading journey!')


def print_error(message: str) -> None:
    """ Print an error message
    Args:
        message (str): error message to print
    """
    print(f'Error: {message}', file=sys.stderr)


def print_menu() -> None:
    """ Print the menu """
    print('Type any of the following commands, or you can type the number.')
    print('1. Search - search your target book by id, author or name. For example - search name harry potter')
    print('2. Recommend - show books with best reviews in non fiction and fiction genres. For example - recommend fiction)')
    print('3. Bookshelf - show books you collect.')
    print('4. Help - Type "help" to get a list of commands.')
    print('5. Exit - exit the program. It will automatically update books info.')
    print()


def get_user() -> str: 
    """ Get the user_name
    Returns:
        user_name (str)
    """
    user_name = input("Please enter a user name: ").strip()
    print()
    return user_name


def get_rate() -> int: 
    """ Get the rate
    Returns:
        rate (int)
    """
    rate = input(
        'Would you like to rate this book? (hit return for blank): ').strip()
    return rate


def get_comment() -> str: 
    """ Get the comment
    Returns:
        comment (str)
    """
    comment = input(
        'Would you like to leave a comment? (hit return for blank): ').strip()
    return comment


def collect_book() -> str:  
    """ Get the command that whether to add to bookshelf
    Returns:
        collect (str): "y" or "n"
    """
    collect = input(
        'Would you like to collect this book? "y" for Yes, "n" for No: ').strip()
    return collect.lower()


def display_book(book: books_utils.Book) -> None: 
    """ Display a detailed book profile including name, author, genre, rating, 
        reviews, intro, and users' ratings and comments
    
    Args:   
        book (books_utils.Book)
    """
    print()
    print(book.name)
    print(f"by {book.author}     {book.genre}")
    print(f"Rating: {book.rating}     {book.reviews} people rate")
    print("-" * 110)
    if len(book.intro) > 0:
        print("Intro")
        print(book.intro)
        print("-" * 110)
    if len(book.comments) > 0:
        print("Comments")
        for key, value in book.comments.items():
            try:
                rate, comment = value.split(' ', 1)
                stars = int(rate) * '*'
                print(f"{key}     {stars}")
                print(comment)
                print()
            except ValueError:
                if value.isnumeric():
                    stars = int(value) * '*'
                    print(f"{key}     {stars}")
                    print()
                elif len(value) > 1:
                    print(key)
                    print(value)
                    print()


def multi_search(books_list: books_utils.BookList) -> books_utils.Book: 
    """ When there are multiple search results, help the user to target 
        one book by id
    
    Args:   
        books_list (books_utils.BookList) 
        
    Return: 
        books_utils.Book: Should always be one book, since the id is unique
    """
    id = int(input("Enther a book id to jump to the detail page: ").strip())
    book = books_list.find_by_id(id)
    return book[0]


def display_board(board: List[books_utils.Book], rank: int = 10) -> None: 
    """ Display recommended books list
    
    Args:   
        board (List[books_utils.Book]) 
        rank (int): defaults to 10, show 10 books
    """
    if len(board) == 0:
        print_error("Wrong genre")
    for book in board:
        print(book)
        print()


def display_search(result: List[books_utils.Book]) -> None: 
    """ Display search results
    
    Args:   
        result (List[books_utils.Book]) 
    """
    print(f"{len(result)} results found")
    for book in result:
        print(book)
        print()


def display_shelf(user: users_utils.User, shelf: books_utils.BookShelf) -> None:  
    """ Display bookshelf
    
    Args:   
        user (users_utils.User)  
        shelf (books_utils.BookShelf)
    """
    print(f"{shelf.name}'s bookshelf")
    if user.name == shelf.name:  
        # Use book id as the match key, if the book id is the same in both user and book side, 
        # add rate information to bookshelf.
        for key, value in shelf.collects.items():
            if key in user.rates:
                rate = user.rates[key]
                print(f"{key}     {value} | your rate: {rate}")
            else:
                print(f"{key}     {value}")
            print()
    return None


def get_command() -> Union[Tuple[Menu, Union[Tuple, str]], str]:
    """ Get the command from the user
    Return:
       tuple: command, args (if any)
    """
    commands = input('What would you like to do? ').strip()
    commands = commands.lower()
    list = commands.split(' ', 1)
    command = list[0]
    if command == 'search' or command == '1':
        value_list = list[1].split(' ', 1)
        if len(value_list) == 2:
            return (Menu.SEARCH, tuple(value_list))
        else:
            print('Please enter in the correct format: 1/search id/author/name value.')
    elif command == 'recommend' or command == '2':
        if len(list) == 2:
            return (Menu.RECOMMEND, list[1])
        else:
            print('Please enter in the correct format: 2/recommend fiction/non fiction.')
    elif command == 'bookshelf' or command == '3':
        return Menu.BOOKSHELF
    elif command == 'help' or command == '4':
        return Menu.HELP
    elif command == 'exit' or command == '5':
        return Menu.EXIT
    else:
        return Menu.UNKNOWN
