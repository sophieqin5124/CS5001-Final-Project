""" 
This is the main entry point for the application. 

NAME: Tianzi Qin
SEMESTER: Spring 23
"""
import books_utils
import users_utils
import view
from typing import Tuple


def run_search(books_list: books_utils.BookList, args: Tuple) -> books_utils.Book: 
    """ Handle situations that show one search result and multiple search results
    
    Args:   
        books_list (books_utils.BookList)   
        args (tuple): search condition
        
    Return: 
        book (books_utils.Book): Should always be one book, since the id is unique
    """
    try:
        type = args[0]
        value = args[1]
        if type == "id":
            result = books_list.find_by_id(value)
        if type == "name":
            result = books_list.find_by_name(value)
        if type == "author":
            result = books_list.find_by_author(value)
        if len(result) == 1:
            book = result[0]
        elif len(result) > 1:
            view.display_search(result)
            search_list = books_utils.BookList(result)
            book = view.multi_search(search_list)
        view.display_book(book)
        return book
    except:
        view.print_error(
            "No eligible results, please check your search condition. ")


def run_bookinfo(user: users_utils.User, book: books_utils.Book,
                 shelf: books_utils.BookShelf) -> None: 
    """ Handle all operations after enter the book profile, including adding rate and comment, 
        add to bookshelf
    
    Args:   
        user (users_utils.User)  
        book (books_utils.Book)   
        shelf (books_utils.BookShelf)
    """
    rate = view.get_rate()
    comment = view.get_comment()
    if rate.isnumeric():
        number = int(rate)
        user.add_rate(book.id, number)
        book.change_rating(number)
    else:
        rate = ''
    if len(comment) > 0:
        user.add_comment(book.id, comment)
    else:
        comment = ''
    if (rate == '') & (comment == ''):
        pass
    else:
        book.add_comment(user.name, rate, comment)
        view.display_book(book)
    collect = view.collect_book()
    if collect == "y":
        shelf.add_collect(book)


def main():  
    """
    This is the main entry point for the application.
    """
    view.print_welcome()
    user_name = view.get_user()
    user = users_utils.User(user_name)
    books_list = books_utils.load_books('data/books.xlsx')
    shelf = books_utils.BookShelf(user.name)
    view.print_help()
    done = False
    while not done:
        commands = view.get_command()
        if isinstance(commands, tuple):
            command, args = commands
        else:
            command = commands
        if command == view.Menu.SEARCH:
            book = run_search(books_list, args)
            if book:
                run_bookinfo(user, book, shelf)
        elif command == view.Menu.RECOMMEND:
            board = books_list.top_books(args)
            view.display_board(board)
        elif command == view.Menu.BOOKSHELF:
            view.display_shelf(user, shelf)
        elif command == view.Menu.HELP:
            view.print_menu()
        elif command == view.Menu.EXIT:
            done = True
        else:
            view.print_error(f"Unknown command")
            view.print_menu()
    books_utils.save_books('data/books.xlsx', books_list)
    view.print_goodbye()


if __name__ == "__main__":
    main()
