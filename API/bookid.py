import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException, JSONDecodeError
from typing import Any
from time import sleep

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
TIME = 3
RETRIES = 5

class BookInfoJSON:
    def __init__(self, base_url: str, target_book_name: str, headers: dict[str, str], cookies: str):
        self.base_url = base_url
        self.target_book_name = target_book_name
        self.headers = headers
        self.cookies = cookies

    @classmethod
    def create(cls, base_url: str, target_book_name: str, headers: dict[str, str] = None, cookies: str = None):
        # 初始化Headers
        if headers is None:
            headers = {}

        if 'User-Agent' not in headers:
            headers['User-Agent'] = USER_AGENT

        # 初始化Cookies
        if not cookies:
            cookies = cls.initialize_get_cookies(cls, base_url=base_url, headers=headers)
            if not cookies:
                return None

        headers['Cookie'] = cookies

        return cls(base_url, target_book_name, headers, cookies)
    
    def get_book_info_json(self)->str | None:
        """get the book info json from api

        Returns
        -------
        str | None
            return func result status
        """             
        query = self.make_query(self.target_book_name)
        search_url = self.base_url + "/api/store/search"
        # 请求API搜索结果
        for retry_count in range(RETRIES):
            try:      
                the_book_info_json = requests.get(url=search_url, headers=self.headers, params=query, timeout=3)
                the_book_info_json.raise_for_status()
                break
            except Timeout as timeout_error:
                if retry_count == RETRIES - 1:
                    print(f"Timeout error occured: {timeout_error}")
                    return None
                
                delay = 2 * (retry_count + 1)
                sleep(delay)
            except HTTPError as http_err:
                if retry_count == RETRIES - 1:
                    print(f'HTTP error occurred: {http_err}')
                    return None
                
                delay = 2 * (retry_count + 1)
                sleep(delay)
            except ConnectionError as conn_err:
                if retry_count == RETRIES - 1:
                    print(f'Connection error occurred: {conn_err}')
                    return None
                
                delay = 2 * (retry_count + 1)
                sleep(delay)
            except RequestException as req_err:
                if retry_count == RETRIES - 1:
                    print(f'An error occurred: {req_err}') 
                    return None

                delay = 2 * (retry_count + 1)
                sleep(delay)
        # 解析返回的JSON文件
        try:
            self.json_result = the_book_info_json.json()
        except JSONDecodeError as jsondecode_error:
            print(f'Timeout error occurred: {jsondecode_error}')
            return None

        with open("cache/bookinfo.json", "wb") as f:
            f.write(the_book_info_json.content)

        return "OK"

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
    
    def initialize_get_cookies(self, base_url: str, headers: dict[str, str])->str | None:
        """initialize the requests cookies

        Parameters
        ----------
        base_url : str
            the base url to get
        headers : dict[str, str]
            the requests headers

        Returns
        -------
        str | None
            requests cookies
        """ 
        # 尝试连接weread获取cookies，如果无法连接则报错
        for retry_count in range(RETRIES):
            try:      
                result = requests.get(url=base_url, headers=headers, timeout=3)
                result.raise_for_status()
                break
            except Timeout as timeout_error:
                if retry_count == RETRIES - 1:
                    print(f"Timeout error occured: {timeout_error}")
                    return None
                
                delay = 2 * (retry_count + 1)
                sleep(delay)
            except HTTPError as http_err:
                if retry_count == RETRIES - 1:
                    print(f'HTTP error occurred: {http_err}')
                    return None
                
                delay = 2 * (retry_count + 1)
                sleep(delay)
            except ConnectionError as conn_err:
                if retry_count == RETRIES - 1:
                    print(f'Connection error occurred: {conn_err}')
                    return None
                
                delay = 2 * (retry_count + 1)
                sleep(delay)
            except RequestException as req_err:
                if retry_count == RETRIES - 1:
                    print(f'An error occurred: {req_err}') 
                    return None

                delay = 2 * (retry_count + 1)
                sleep(delay)

        cookies = ""

        for key, value in result.cookies.items():
            cookies += key + '=' + value + '; '

        return cookies
    
    def parse_bookid(self, book_info_json: Any = None)->dict[str, str] | None:
        """parse the json of the search result which includes the book infos

        Parameters
        ----------
        book_info_json : Any
            the json created by function `get_book_info_json`

        Returns
        -------
        dict[str, str] | None
            the book names and book ids, like {book_name: book_id}
        """        
        book_info_dict = {}

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
                book_info_dict.update({book_name: book_id})
        
        if book_info_dict != {}:
            return book_info_dict
        else:
            print("Error: can't find book in the search result JSON!")
            return None

# <--- Usage Example --->
if __name__ == "__main__":
    info = BookInfoJSON.create("https://weread.qq.com", "百年孤独")
    info.get_book_info_json()
    all_book_info = info.parse_bookid()

    for key, value in all_book_info.items():
        print("book name: {}\nbook id: {}\n\n".format(key, value))