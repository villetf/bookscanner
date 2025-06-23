def getGoogleBooksData(isbn):
   import urequests
   import json

   url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
   response = urequests.get(url)

   if response.status_code == 200:

      data = response.json()
      response.close()
      if "items" in data and len(data["items"]) > 0:
         book = data["items"][0]  # första träffen
         volume_info = book.get("volumeInfo", {})
         title = volume_info.get("title", "Ingen titel hittades")
         print("Titel:", title)
      else:
         print("Inga böcker hittades för detta ISBN.")

   else:
      print(f"Error: {response.status_code}")
      response.close()
      return None
   