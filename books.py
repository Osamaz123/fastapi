from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'Title one', 'author': 'Author one', 'category': 'science'},
    {'title': 'Title two', 'author': 'Author two', 'category': 'science'},
    {'title': 'Title three', 'author': 'Author three', 'category': 'history'},
    {'title': 'Title four', 'author': 'Author four', 'category': 'maths'},
    {'title': 'Title five', 'author': 'Author five', 'category': 'maths'},
    {'title': 'Title six', 'author': 'Author two', 'category': 'maths'}


]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_title}")
async def read_books(book_title: str):
    return [book for book in BOOKS if book.get('title').casefold() == book_title.casefold()]
    
@app.get('/books/')
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    
    return books_to_return

@app.get("/books/byauthor/")
async def read_books_by_author_path(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)

    return books_to_return


            
@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
                  book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    
    return books_to_return


@app.post("/books/create_book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)



@app.put("/books/update_book")
async def update_book(updated_book= Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break


'''
get all books from specific author using path or query parameters
'''


@app.get("/books/byauthor/{author}")
async def read_books_by_author_path(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)

    return books_to_return


            

