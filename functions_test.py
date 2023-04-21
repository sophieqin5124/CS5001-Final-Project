from books_utils import Book, BookList, BookShelf, load_books, save_books
from users_utils import User
from io import StringIO
from unittest.mock import patch
import sys
import view
import run
import unittest
import pandas as pd


class Test_books_utils(unittest.TestCase):
    """ Test all functions in books_utils """

    def test_Book_init(self):
        """ Test Book.__init__  with 
             id: 1 
             name: book1 
             author: any 
             rating: 5 
             reviews: 10 
             genere: Fiction 
             intro: test 
             comments: '{"sophie":"5}'"""
        case = Book(1, 'book1', 'any', 5, 10, 'Fiction',
                    'test', '{"sophie": "5 test"}')
        self.assertEqual(case.id, 1)
        self.assertEqual(case.name, 'book1')
        self.assertEqual(case.author, 'any')
        self.assertEqual(case.rating, 5)
        self.assertEqual(case.reviews, 10)
        self.assertEqual(case.genre, 'Fiction')
        self.assertEqual(case.intro, 'test')
        # json_load
        self.assertEqual(case.comments, {'sophie': '5 test'})

    def test_Book_score(self):
        """ Test Book.score """
        case = Book(1, 'book1', 'any', 5, 10, 'Fiction')
        self.assertAlmostEqual(case.score, 6.5)

    def test_Book_change_rating(self):
        """ Test Book.change_rating with a new rate 4"""
        case = Book(1, 'book1', 'any', 5, 10, 'Fiction')
        case.change_rating(4)
        self.assertAlmostEqual(case.rating, 4.9)

    def test_Book_add_comment(self):
        """ Test Book.add_comment """
        case = Book(1, 'book1', 'any', 5, 10, 'Fiction')
        case.add_comment("sophie", "5", "test")
        self.assertAlmostEqual(case.comments, {'sophie': '5 test'})

    def test_Book_str(self):
        """ Test Book.__str__ """
        case = Book(1, 'book1', 'any', 5, 10, 'Fiction')
        string = "Id: 1 Name: book1\nAuthor: any\nRating: 5  Reviews: 10"
        self.assertAlmostEqual(str(case), string)

    def setUp(self):
        """Set up a test list for all BookList tests"""
        self.book1 = Book(1, 'Becoming', 'Michelle Obama',
                          4.8, 62, 'Non Fiction', 'test')
        self.book2 = Book(2, 'Educated: A Memoir',
                          'Tara Westover', 4.7, 29, 'Non Fiction', 'test')
        self.book3 = Book(3, "The Handmaid's Tale",
                          'Margaret Atwood', 4.3, 30, 'Fiction', 'test')
        self.book4 = Book(4, 'The Hunger Games (Book 1)',
                          'Suzanne Collins', 4.7, 33, 'Fiction', 'test')
        self.book5 = Book(5, 'The Hunger Games Trilogy Boxed Set',
                          'Suzanne Collins', 4.8, 17, 'Fiction', 'test')
        self.book6 = Book(6, 'Unbroken', 'Laura Hillenbrand',
                          4.8, 30, 'Non Fiction', 'test')
        self.items = [self.book1, self.book2, self.book3,
                      self.book4, self.book5, self.book6]
        self.sample = BookList(self.items)

    def test_BookList_init(self):
        """ Test BookList.__init__  with self.sample """
        self.assertEqual(self.sample.books, self.items)

    def test_BookList_top_books(self):
        """ Test BookList.top_books with  
            self.sample and fiction genre
        """
        board = self.sample.top_books("fiction", 3)
        expect = [self.book4, self.book3, self.book5]
        self.assertEqual(board, expect)

    def test_BookList_find_by_id(self):
        """ Test BookList.find_by_id with  
            self.sample and id: 1
        """
        result = self.sample.find_by_id('1')
        expect = [self.book1]
        self.assertEqual(result, expect)

    def test_BookList_find_by_name(self):
        """ Test BookList.find_by_name with  
            self.sample and short_name: hunger game
        """
        result = self.sample.find_by_name('hunger game')
        expect = [self.book4, self.book5]
        self.assertEqual(result, expect)

    def test_BookList_find_by_author(self):
        """ Test BookList.find_by_author with  
            self.sample and short author name: Suzanne
        """
        result = self.sample.find_by_author('Suzanne')
        expect = [self.book4, self.book5]
        self.assertEqual(result, expect)

    def test_BookShelf_init(self):
        """ Test BookShelf.__init__ with name: test """
        case = BookShelf('test')
        self.assertEqual(case.name, 'test')
        self.assertEqual(len(case.collects), 0)

    def test_BookShelf_add_collect(self):
        """ Test BookShelf.add_collect with self.book1 """
        case = BookShelf('test')
        case.add_collect(self.book1)
        self.assertEqual(case.collects, {self.book1.id: self.book1.name})

    def test_load_books(self):
        """ Test load_books with  
            self.items and test_file.xlsx
        """
        data = load_books('data/test_file.xlsx')
        self.assertEqual(len(data.books), len(self.items))
        self.assertEqual(str(self.book1), str(data.books[0]))
        self.assertEqual(str(self.book2), str(data.books[1]))
        self.assertEqual(str(self.book3), str(data.books[2]))
        self.assertEqual(str(self.book4), str(data.books[3]))
        self.assertEqual(str(self.book5), str(data.books[4]))
        self.assertEqual(str(self.book6), str(data.books[5]))

    def test_save_books(self):
        """ Test save_books with test_file.csv,  
            compare it with the file where save self.sample to 
        """
        save_books('data/test_file_2.xlsx', self.sample)
        df1 = pd.read_excel('data/test_file.xlsx')
        df2 = pd.read_excel('data/test_file_2.xlsx')
        diff = pd.concat([df1, df2]).drop_duplicates(keep=False)
        self.assertEqual(diff.shape[0], 0)


class Test_users_utils(unittest.TestCase):
    """ Test all functions in users_utils """

    def test_User_init(self):
        """ Test User.__init__  with name: Sophie """
        case = User('Sophie')
        self.assertEqual(case.name, 'Sophie')
        self.assertEqual(len(case.rates), 0)
        self.assertEqual(len(case.comments), 0)

    def test_User_add_rate(self):
        """ Test User.add_rate with 
             id: 1 rate: 10 
             id: 2 rate: -5 
        """
        case = User('Sophie')
        case.add_rate(1, 10)
        case.add_rate(2, -5)
        self.assertEqual(case.rates[1], 5)
        self.assertEqual(case.rates[2], 1)

    def test_User_add_comment(self):
        """ Test User.add_comment with 
             id: 1 comment: 'test'
        """
        case = User('Sophie')
        case.add_comment(1, 'test')
        self.assertEqual(case.comments[1], 'test')


class Test_view_run(unittest.TestCase):
    """ Test all functions in view and run """

    def test_Menu(self):
        """ Test view.Menu """
        self.assertEqual(view.Menu(1), view.Menu.SEARCH)
        self.assertEqual(view.Menu(2), view.Menu.RECOMMEND)
        self.assertEqual(view.Menu(3), view.Menu.BOOKSHELF)
        self.assertEqual(view.Menu(4), view.Menu.HELP)
        self.assertEqual(view.Menu(5), view.Menu.EXIT)
        self.assertEqual(view.Menu(6), view.Menu.UNKNOWN)

    def test_print_welcome(self):
        """ Test view.print_welcome """
        buffer = StringIO()
        sys.stdout = buffer
        view.print_welcome()
        output = buffer.getvalue().strip()
        sys.stdout = sys.__stdout__
        self.assertEqual(output, 'Welcome to Find Your Book!')

    def test_print_help(self):
        """ Test view.print_help """
        buffer = StringIO()
        sys.stdout = buffer
        view.print_help()
        output = buffer.getvalue().strip()
        sys.stdout = sys.__stdout__
        self.assertEqual(output, 'Type "help" to get a list of commands.')

    def test_print_goodbye(self):
        """ Test view.print_goodbye """
        buffer = StringIO()
        sys.stdout = buffer
        view.print_goodbye()
        output = buffer.getvalue().strip()
        sys.stdout = sys.__stdout__
        self.assertEqual(output, 'Enjoy your reading journey!')

    def test_print_error(self):
        """ Test view.print_error """
        buffer = StringIO()
        sys.stderr = buffer
        view.print_error('test')
        output = buffer.getvalue().strip()
        sys.stderr = sys.__stderr__
        self.assertEqual(output, 'Error: test')

    def test_print_menu(self):
        """ Test view.print_menu """
        buffer = StringIO()
        sys.stdout = buffer
        view.print_menu()
        output = buffer.getvalue().strip()
        sys.stdout = sys.__stdout__
        expect = 'Type any of the following commands, or you can type the number.\n'
        expect += '1. Search - search your target book by id, author or name. For example - search name harry potter\n'
        expect += '2. Recommend - show books with best reviews in non fiction and fiction genres. For example - recommend fiction)\n'
        expect += '3. Bookshelf - show books you collect.\n'
        expect += '4. Help - Type "help" to get a list of commands.\n'
        expect += '5. Exit - exit the program. It will automatically update books info.'
        self.assertEqual(output, expect)

    @patch('builtins.input', side_effect=['test'])
    def test_get_user(self, mock_input):
        """ Test view.get_user """
        user_name = view.get_user()
        self.assertEqual(user_name, 'test')

    @patch('builtins.input', side_effect=['test'])
    def test_get_comment(self, mock_input):
        """ Test view.get_comment """
        comment = view.get_comment()
        self.assertEqual(comment, 'test')

    @patch('builtins.input', side_effect=['y'])
    def test_collect_book(self, mock_input):
        """ Test view.collect_book """
        result = view.get_comment()
        self.assertEqual(result, 'y')

    def test_display_book(self):
        """ Test view.display_book """
        buffer = StringIO()
        sys.stdout = buffer
        case = Book(1, 'book1', 'any', 5, 10, 'Fiction',
                    'test', '{"sophie": "5 test"}')
        view.display_book(case)
        output = buffer.getvalue().strip()
        sys.stdout = sys.__stdout__
        expect = 'book1\n'
        expect += 'by any     Fiction\n'
        expect += 'Rating: 5     10 people rate\n'
        expect = expect + '-' * 110 + '\n'
        expect = expect + 'Intro\n' + 'test\n' + '-' * 110 + '\n'
        expect = expect + 'Comments\n' + 'sophie     *****\n' + 'test'
        self.assertEqual(output, expect)

    def setUp(self):
        """Set up a test list for all view and run tests"""
        self.book1 = Book(1, 'Becoming', 'Michelle Obama',
                          4.8, 62, 'Non Fiction', 'test')
        self.book2 = Book(2, 'Educated: A Memoir',
                          'Tara Westover', 4.7, 29, 'Non Fiction', 'test')
        self.book3 = Book(3, "The Handmaid's Tale",
                          'Margaret Atwood', 4.3, 30, 'Fiction', 'test')
        self.book4 = Book(4, 'The Hunger Games (Book 1)',
                          'Suzanne Collins', 4.7, 33, 'Fiction', 'test')
        self.book5 = Book(5, 'The Hunger Games Trilogy Boxed Set',
                          'Suzanne Collins', 4.8, 17, 'Fiction', 'test')
        self.book6 = Book(6, 'Unbroken', 'Laura Hillenbrand',
                          4.8, 30, 'Non Fiction', 'test')
        self.items = [self.book1, self.book2, self.book3,
                      self.book4, self.book5, self.book6]
        self.sample = BookList(self.items)

    @patch('builtins.input', side_effect=['1'])
    def test_multi_search(self, mock_input):
        """ Test view.multi_search """
        result = view.multi_search(self.sample)
        self.assertEqual(str(result), str(self.book1))

    def test_display_board(self):
        """ Test view.display_board with top2 fictions and invalid genre """
        buffer = StringIO()
        sys.stdout = buffer
        board = self.sample.top_books("Fiction", 2)
        view.display_board(board)
        expect = str(self.book4) + '\n\n'
        expect += str(self.book3)
        output = buffer.getvalue().strip()
        sys.stdout = sys.__stdout__
        self.assertEqual(output, expect)

        buffer = StringIO()
        sys.stderr = buffer
        board = self.sample.top_books("invalid", 2)
        view.display_board(board)
        output = buffer.getvalue().strip()
        sys.stderr = sys.__stderr__
        self.assertEqual(output, "Error: Wrong genre")

    def test_display_search(self):
        """ Test view.display_search with search name: hunger game """
        buffer = StringIO()
        sys.stdout = buffer
        result = self.sample.find_by_name('hunger game')
        view.display_search(result)
        expect = '2 results found\n'
        expect = expect + str(self.book4) + '\n' + '\n'
        expect += str(self.book5)
        output = buffer.getvalue().strip()
        sys.stdout = sys.__stdout__
        self.assertEqual(output, expect)

    def test_display_shelf(self):
        """ Test view.display_shelf"""
        buffer = StringIO()
        sys.stdout = buffer
        user = User('Sophie')
        case = BookShelf(user.name)
        case.add_collect(self.book1)
        case.add_collect(self.book2)
        user.add_rate(1, 5)
        view.display_shelf(user, case)
        output = buffer.getvalue().strip()
        sys.stdout = sys.__stdout__
        expect = "Sophie's bookshelf\n"
        expect += "1     Becoming | your rate: 5\n\n"
        expect += "2     Educated: A Memoir"
        self.assertEqual(output, expect)

    @patch('builtins.input', side_effect=['1 name Harry Potter', '1 author', '2 Fiction'])
    def test_get_command(self, mock_input):
        """ Test view.get_command """
        # input: 1 name Harry Potter
        result1 = view.get_command()
        expect = (view.Menu.SEARCH, ('name', 'harry potter'))
        self.assertEqual(result1, expect)

        # input: 1 author
        result2 = view.get_command()
        expect = None
        self.assertEqual(result2, expect)

        # input: 2 Fiction
        result3 = view.get_command()
        expect = (view.Menu.RECOMMEND, 'fiction')
        self.assertEqual(result3, expect)

    @patch('builtins.input', side_effect=['4'])
    def test_run_search(self, mock_input):
        """ Test run.run_search """
        # multi search case
        book1 = run.run_search(self.sample, ('name', 'hunger game'))
        self.assertEqual(str(book1), str(self.book4))

        book2 = run.run_search(self.sample, ('id', '1'))
        self.assertEqual(str(book2), str(self.book1))

    @patch('builtins.input', side_effect=['5', 'A good book', 'y'])
    def test_run_bookinfo(self, mockinput):
        """ Test run.bookinfo """
        user = User('Sophie')
        book = self.book1
        shelf = BookShelf(user.name)
        run.run_bookinfo(user, book, shelf)
        expect = "Id: 1 Name: Becoming\nAuthor: Michelle Obama\nRating: 4.8  Reviews: 63"
        self.assertEqual(str(book), expect)
        self.assertEqual(shelf.collects[1], 'Becoming')


def run_tests():
    unittest.main(verbosity=3)


run_tests()
