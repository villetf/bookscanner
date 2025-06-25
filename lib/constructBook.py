


from Book import Book


def constructBook(isbn, googleData, openLibraryData):
   newBook = Book(
      isbn = int(isbn),
      title = googleData.get("title", ""),
      author = googleData.get("authors", []),
      yearWritten = googleData.get("publishedDate", None),
      language = googleData.get("language", ""),
      originalLanguage = "",
      genre = "",
      format = "",
      imageUrl = openLibraryData.get("cover", {}).get("large", "")
   )

   if newBook.title == "" and openLibraryData['title']:
      newBook.title = openLibraryData['title']

   if newBook.author == [] and openLibraryData['authors']:
      newBook.author = [author['name'] for author in openLibraryData['authors']]

   if newBook.yearWritten != None:
      newBook.yearWritten = int(newBook.yearWritten)

   if newBook.language == "en":
      newBook.language = "Engelska"
   elif newBook.language == "sv":
      newBook.language = "Svenska"

   return newBook

   