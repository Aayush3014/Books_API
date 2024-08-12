import requests

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

def fetch_books(query, filter_type=""):
    params = {"q": query, "key": "AIzaSyDWcB4YLmrQQ3cQBGgOKdYL4DL4Ji6CDCE"}
    if filter_type:
        params["filter"] = filter_type
    try:
        response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_book_details(book_id):
    url = f"{GOOGLE_BOOKS_API_URL}/{book_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    