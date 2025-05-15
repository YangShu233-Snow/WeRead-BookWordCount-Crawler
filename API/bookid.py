import requests
import json
from typing import Any

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"

class BookInfoJSON:
    def __init__(self, base_url: str, target_book_name: str, headers: dict[str, str] = None,  cookies: str = None):
        
        self.base_url = base_url
        self.target_book_name = target_book_name
        
        # 初始化Headers
        if headers is None:
            headers = {}

        if headers.get('User-Agent', None):
            self.headers = headers
        else:
            headers.update({'User-Agent': USER_AGENT})
            self.headers = headers
        
        # 初始化Cookie
        if cookies != "":
            headers.update({'Cookie': cookies})
            self.headers = headers
        else:
            cookies = self.initialize_get_cookies(base_url=self.base_url, headers=self.headers)
            headers.update({'Cookie': cookies})
            self.headers = headers
    
    def get_book_info_json(self):
        """get the book info json from api
        """        
        query = self.make_query(self.target_book_name)
        search_url = self.base_url + "/api/store/search"
        the_book_info_json = requests.get(url=search_url, headers=self.headers, params=query)
        self.json_result = the_book_info_json.json()

        with open("cache/bookinfo.json", "wb") as f:
            f.write(the_book_info_json.content)

    def make_query(self, target_book_name: str) ->dict[str, str]:
        """constrcut a dict query for search url construction

        Parameters
        ----------
        target_book_name : str
            the book name you want to search

        Returns
        -------
        dict[str, str]
            return the {'keyword': target_book_name}
        """        
        return {'keyword': target_book_name}
    
    def initialize_get_cookies(self, base_url: str, headers: dict[str, str]):
        """initialize the requests cookies

        Parameters
        ----------
        base_url : str
            the base url to get
        headers : dict[str, str]
            the requests headers

        Returns
        -------
        str
            requests cookies
        """       
        result = requests.get(url=base_url, headers=headers)
        cookies = ""

        for key, value in result.cookies.items():
            cookies += key + '=' + value + '; '

        return cookies
    
    def parse_bookid(self, book_info_json: Any = None)->dict[str, str]:
        """parse the json of the search result which includes the book infos

        Parameters
        ----------
        book_info_json : Any
            the json created by function `get_book_info_json`

        Returns
        -------
        dict[str, str]
            the book names and book ids, like {book_name: book_id}
        """        
        book_info_list = []

        # 初始化书籍信息的JSON
        if book_info_json == None:
            book_info_json = self.json_result
        
        results = book_info_json["results"]

        # 遍历API返回的JSON中，对应最终页面的每一块的标题是否是“电子书”
        for block in results:
            if block["title"] != "电子书":
                continue
            
            books = block["books"]

            # 遍历电子书中，books内的每一本书的信息，并提取
            for book in books:
                book_info = book["bookInfo"]
                book_id = book_info["bookId"]
                book_name = book_info["title"]
                book_info_list.append((book_name, book_id))

        return dict(book_info_list)

# <--- Usage Example --->
if __name__ == "__main__":
    info = BookInfoJSON("https://weread.qq.com", "百年孤独")
    info.get_book_info_json()
    all_book_info = info.parse_bookid()

    for key, value in all_book_info.items():
        print("book name: {}\nbook id: {}\n\n".format(key, value))