""" 
user_utils handles user related classes and functions,   
we can use them to save a user name, record user's rates and comments 
to different books.

Classes included: User

NAME: Tianzi Qin
SEMESTER: Spring 23
"""
class User:
    """A user class contains the following properties:

    Attributes: 
        name (str) - a name for the user
        rates (dict): An empty dict, save users'rates, format: {book id: rate}  
        comments (dict): An empty dict, save users'comments, format: {book id: comment} 
    """

    def __init__(self, name: str):
        """ Constructor of the User object. 
        
        Args: 
            name (str): A name for the user
        """ 
        self.name = name
        self.rates = {}
        self.comments = {}

    def add_rate(self, id: int, value: int, min: int = 1, max: int = 5) -> None: 
        """ Add rate to rates dict 
        
        Args:  
            id (int): unique book id  
            value (str): user's rate 
            min (int): defaults to 1, minimum rate 
            max (int): defaults to 5, maximum rate 
        """     
        if value < min:
            value = min
        if value > max:
            value = max
        self.rates[id] = value

    def add_comment(self, id: int, comment: str) -> None: 
        """ Add comment to comments dict 
        
        Args:  
            id (int): unique book id  
            comment (str): user's comment
        """ 
        self.comments[id] = comment
