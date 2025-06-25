import urequests



def getGoogleBooksData(isbn):
   url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
   response = urequests.get(url)

   print('inne i google')

   if response.status_code == 200:
      data = response.json()
      response.close()
      if "items" in data and len(data["items"]) > 0:
         book = data["items"][0]
         bookInfo = book.get("volumeInfo", {})
         return bookInfo
      else:
         return {}
   else:
      print(f"Error: {response.status_code}")
      response.close()
      return None
   

def getOpenLibraryData(isbn):
   url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
   response = urequests.get(url)

   if response.status_code == 200:
      data = response.json()
      response.close()
      if f"ISBN:{isbn}" in data:
         bookInfo = data[f"ISBN:{isbn}"]
         return bookInfo
      else:
         return data
   else:

      print(f"Error: {response.status_code}")
      response.close()
      return None
   