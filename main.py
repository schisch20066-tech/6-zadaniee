from fastapi import FastAPI, Query

app = FastAPI()

@app.get('/')
async def home():
    return {'Hello!': 'This is a test GET-request to the API'}
bookshelf = {
       1: {
           'book': 'Ulyss',
           'price': 4.75,
           'author': 'James Joyce'
       },

       2: {
           'book': 'Three Men in a Boat (To Say Nothing of the Dog)',
           'price': 3.99,
           'author': 'Jerome K. Jerome'
       }
   }
@app.get('/get-book/{book_id}')
async def get_book(book_id: int):
   return bookshelf[book_id]
from typing import Optional
from pydantic import BaseModel
class BookInfo(BaseModel):
   book: str
   price: float
   author: Optional[str] = None
@app.post('/create-book/{book_id}')
async def create_book(book_id: int, new_book: BookInfo):
   if book_id in bookshelf:
       return {'Error': 'Book already exists'}
   bookshelf[book_id] = new_book
   return bookshelf[book_id]
class UpdateBook(BaseModel):
   book: Optional[str] = None
   price: Optional[float] = None
   author: Optional[str] = None
@app.put('/update-book/{book_id}')
async def update_book(book_id: int, upd_book: UpdateBook):
   if book_id not in bookshelf:
       return {'Error': 'Book ID does not exists'}
   if upd_book.book != None:
       bookshelf[book_id].book = upd_book.book
   if upd_book.price != None:
       bookshelf[book_id].price = upd_book.price
   if upd_book.author != None:
       bookshelf[book_id].author = upd_book.author
   return bookshelf[book_id]
book_id: int = Query(..., description='The book ID must be greater than zero')
@app.delete('/delete-book')
def delete_book(book_id: int = Query(..., description='The book ID must be greater than zero')):
   if book_id not in bookshelf:
       return {'Error': 'Book ID does not exists'}
   del bookshelf[book_id]
   return {'Done': 'The book successfully deleted'}