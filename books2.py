from typing import Dict, Optional, Any
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status


app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int


    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date
    
class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)


    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2029

            }
        }
    }




BOOKS = [
    Book (1, 'Computer Science Pro', 'codingwithcoby', 'A very nice book!', 5,2030),
    Book (2, 'Be Fast with FastAPI', 'codingwithcoby', 'A great book!',3, 2030),
    Book (3, 'Master Endpoints', 'codingwithroby', 'A awesome book!',3, 2029),
    Book (4, 'HP1', 'Author 1', 'Book Description',4, 2028),
    Book (5, 'HP2', 'Author 2', 'Book Description',5, 2027),
    Book (6, 'HP3', 'Author 3', 'Book Description',4, 2026)
]




@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    """Fetches and returns all books from the collection."""
    return BOOKS


# path param
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    """Fetches a book by its ID.

    Args:
        book_id (int): The ID of the book to fetch.

    Returns:
        Book: The book matching the provided ID.
    """

    for book in BOOKS:
        if book.id == book_id:
            return book
    # Http exception
    raise HTTPException(status_code=404, detail='Item not found')


# query param
@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    """Fetches books with a specific rating.

    Args:
        book_rating (int): The rating to filter books by.

    Returns:
        List[Book]: List of books with the specified rating.
    """
    books_to_read = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_read.append(book)

    return books_to_read


@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_books_by_publish_date(published_date:int = Query(gt=1999, lt=2031)):
    """Fetches books published in a specific year.

    Args:
        published_date (int): The year to filter books by.

    Returns:
        List[Book]: List of books published in the specified year.
    """
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
        
    return books_to_return




@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    """Creates a new book and adds it to the collection.

    Args:
        book_request (BookRequest): The details of the book to create.
    """
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id +1

    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    """Updates an existing book's details.

    Args:
        book (BookRequest): The updated book details.

    Raises:
        HTTPException: If the book to update is not found.
    """
    book_changed=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")


    

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    """Deletes a book by its ID.

    Args:
        book_id (int): The ID of the book to delete.

    Raises:
        HTTPException: If the book to delete is not found.
    """
    book_changed=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break

    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")
    

@app.patch("/books/{book_id}", status_code=status.HTTP_200_OK)
async def patch_book(book_id:int = Path(gt=0), book_update: Dict[str, Optional[Any]] = None):
    """Partially updates a book's details.

    Args:
        book_id (int): The ID of the book to update.
        book_update (Dict[str, Optional[Any]]): The fields to update.

    Returns:
        Book: The updated book.

    Raises:
        HTTPException: If the book to update is not found.
    """
    for i, book in enumerate(BOOKS):
        if book.id == book_id:
            if book_update.get("title"):
                BOOKS[i].title = book_update["title"]
            if book_update.get("author"):
                BOOKS[i].author = book_update["author"]
            if book_update.get("description"):
                BOOKS[i].description = book_update["description"]
            if book_update.get("rating"):
                BOOKS[i].rating = book_update["rating"]
            if book_update.get("published_date"):
                BOOKS[i].published_date = book_update["published_date"]
            return BOOKS[i]
        
    raise HTTPException(status_code=404, detail="Item not found")



