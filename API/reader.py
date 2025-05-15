import lxml.etree
import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException, JSONDecodeError
from requests import Response
import lxml
from lxml import etree
from time import sleep

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
PATTERN = r'(//div[@class="horizontalReaderCoverPage_stats_item_data horizontalReaderCoverPage_stats_item_subTitle_number"])[2]//text()'
TIME = 3
RETRIES = 5

class Reader:
    def __init__(self, base_url: str, reader_id: str, headers: dict[str, str] = None,  cookies: str = None):
        # 构建Reader请求的url
        self.base_url = base_url
        self.reader_url = base_url + "/web/reader/" + reader_id
        self.headers = headers
        self.cookies = cookies

    @classmethod
    def create(cls, base_url: str, reader_id: str, headers: dict[str, str] = None,  cookies: str = None):
        """create a Reader

        Parameters
        ----------
        base_url : str
            the base url to weread
        reader_id : str
            the reader_id encrypted from book_id
        headers : dict[str, str], optional
            the headers to request, by default None
        cookies : str, optional
            the cookies added into headers, by default None
        """        
        # 初始化Headers
        if headers is None:
            headers = {}

        if 'User-Agent' not in headers:
            headers['User-Agent'] = USER_AGENT
        
        # 初始化Cookies
        if not cookies:
            cookies = cls.initialize_get_cookies(base_url=base_url, headers=headers)
            if not cookies:
                return None

        headers['Cookie'] = cookies

        return cls(base_url, reader_id, headers, cookies)
    
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

    def get_book_word_count(self)->str | None:
        """get the target book word count

        Returns
        -------
        str | None
            return the info of the book word count, like "22.8 万字"
        """        
        reader_url = self.reader_url
        results = self.get_reader_page(reader_url, self.headers)

        if results == None:
            return None
        
        if results == []:
            print("Error: can't find the book")
            return None
        
        word_count = results[0] + " " + results[1]

        return word_count
            

    def get_reader_page(self, reader_url: str, headers: dict[str, str])->list[str, str] | None:
        """requests the reader page of the target book

        Parameters
        ----------
        reader_url : str
            the reader page url
        headers : dict[str, str]
            the headers

        Returns
        -------
        list[str, str] | None
            return the results about list[word nums, unit]
        """        
        reader_page_html = requests.get(url=reader_url, headers=headers)
        for retry_count in range(RETRIES):
            try:      
                reader_page_html = requests.get(url=reader_url, headers=headers, timeout=3)
                reader_page_html.raise_for_status()
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

        results = self.parse_reader_page(reader_page_html, pattern=PATTERN)

        return results


    def parse_reader_page(self, reader_page_html: Response, pattern: str)->list[str, str] | None:
        """parse the target reader page and extract the book word counts from it.

        Parameters
        ----------
        reader_page_html : Response
            the target reader page html(from `requests.get()`)
        pattern : str
            the XPath to the word counts

        Returns
        -------
        list[str, str] | None
            return the results including the word number and the unit.
        """
        results = None

        reader_page = reader_page_html.content.decode("utf-8")
        reader_page_node = etree.HTML(reader_page)
        results = reader_page_node.xpath(pattern)
        
        return results

# <--- Usage Example --->
if __name__ == "__main__":
    reader = Reader("https://weread.qq.com", "8bc329705e46708bcb0c164")
    word_count = reader.get_book_word_count()
    print(word_count)