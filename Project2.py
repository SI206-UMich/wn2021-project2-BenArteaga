from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """

    f = open(filename, 'r')
    file_content = f.readlines()
    f.close()
    file_string = ''
    for line in file_content:
        file_string += line
    soup = BeautifulSoup(file_string, 'html.parser')

    # get list of books
    table_tag = soup.find('table', class_='tableList')
    book_tags = table_tag.find_all('tr')
    book_tuples = []

    # loop through all of the books and add a tuple to the list
    for book in book_tags:
        title = book.find('a', class_='bookTitle').text.strip('\n')
        author = book.find('a', class_='authorName').text.strip('\n')
        book_tuple = (title, author)
        book_tuples.append(book_tuple)

    return book_tuples

def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    # create soup object from url
    r = requests.get('https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc')
    soup = BeautifulSoup(r.text, 'html.parser')

    # get all of the book tags on the page
    book_tags = soup.find_all('a', class_='bookTitle')

    # iterate through the first ten and add the url to the list
    urls = []
    i = 0
    for tag in book_tags:
        if i >= 10:
            break
        i += 1
        url = 'https://www.goodreads.com' + tag.get('href')
        urls.append(url)
    
    return urls


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    # create soup object from book url
    r = requests.get(book_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    # get title and author
    left_container_tag = soup.find('div', class_='leftContainer')
    title_tag = left_container_tag.find('h1')
    print(title_tag)
    author_tag = left_container_tag.find('a', class_='authorName')

    # get number of pages
    anchor2 = left_container_tag.find('div', class_='uitext darkGreyText')
    anchor3s = anchor2.find_all('span')
    num_pages = 0
    for tag in anchor3s:
        if tag.get('itemprop') == 'numberOfPages':
            # get the number of pages from the pages_tag
            regex = '\d+'
            num_pages = int(re.findall(regex, tag.text)[0])

    return (title_tag.text, author_tag.text, num_pages)



def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    pass


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    pass


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_links = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        results = get_titles_from_search_results('search_results.htm')

        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(20, len(results))

        # check that the variable you saved after calling the function is a list
        dummy = []
        self.assertEqual(type(dummy), type(results))

        # check that each item in the list is a tuple
        dummy_tuple = ('hello', 'hello')
        for item in results:
            self.assertEqual(type(dummy_tuple), type(item))

        # check that the first book and author tuple is correct (open search_results.htm and find it)
        first_tuple = ('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling')
        self.assertEqual(first_tuple, results[0])

        # check that the last title is correct (open search_results.htm and find it)
        last_tuple = ('Harry Potter: The Prequel (Harry Potter, #0.5)','J.K. Rowling')
        self.assertEqual(last_tuple, results[19])

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        dummy_list = []
        self.assertEqual(type(get_search_links()), type(dummy_list))

        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(get_search_links()), 10)

        dummy_string = 'hello'
        for url in self.search_links:
            # check that each URL in the TestCases.search_urls is a string
            self.assertEqual(type(url), type(dummy_string))
            # check that each URL contains the correct url for Goodreads.com followed by /book/show/
            regex = 'https://www.goodreads.com/book/show/'
            found = re.findall(regex, url)
            self.assertEqual(len(found), 1)
        


    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        summaries = []
        # for each URL in TestCases.search_urls (should be a list of tuples)
        for url in self.search_links:
            summary = get_book_summary(url)
            summaries.append(summary)

        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)

        for summ in summaries:
            # check that each item in the list is a tuple
            dummy_tuple = ('hi', 'hi')
            self.assertEqual(type(summ), type(dummy_tuple))

            # check that each tuple has 3 elements
            self.assertEqual(len(summ), 3)

            # check that the first two elements in the tuple are string
            dummy_string = 'yo'
            self.assertEqual(type(summ[0]), type(dummy_string))
            self.assertEqual(type(summ[1]), type(dummy_string))

            # check that the third element in the tuple, i.e. pages is an int
            dummy_int = 3
            self.assertEqual(type(summ[2]), type(dummy_int))

        # check that the first book in the search has 337 pages
        self.assertEqual(summaries[0][2], 337)


    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable

        # check that we have the right number of best books (20)

            # assert each item in the list of best books is a tuple

            # check that each tuple has a length of 3

        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'

        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        pass

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable

        # call write csv on the variable you saved and 'test.csv'

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)


        # check that there are 21 lines in the csv

        # check that the header row is correct

        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        pass


if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



