import requests
from requests import Response
import lxml
from lxml import etree

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
PATTERN = r'(//div[@class="horizontalReaderCoverPage_stats_item_data horizontalReaderCoverPage_stats_item_subTitle_number"])[2]//text()'

class Reader:
    def __init__(self, base_url: str, reader_id: str, headers: dict[str, str] = None,  cookies: str = None):
        # 构建Reader请求的url
        self.reader_url = base_url + "/web/reader/" + reader_id

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

    def get_book_word_count(self)->str:
        """get the target book word count

        Returns
        -------
        str
            return the info of the book word count, like "22.8 万字"
        """        
        reader_url = self.reader_url
        results = self.get_reader_page(reader_url, self.headers)
        if results != []:
            word_count = results[0] + " " + results[1]
        else:
            word_count = "error: can't find the book"

        return word_count
            

    def get_reader_page(self, reader_url: str, headers: dict[str, str])->list[str, str]:
        """requests the reader page of the target book

        Parameters
        ----------
        reader_url : str
            the reader page url
        headers : dict[str, str]
            the headers

        Returns
        -------
        list[str, str]
            return the results about list[word nums, unit]
        """        
        reader_page_html = requests.get(url=reader_url, headers=headers)
        results = self.parse_reader_page(reader_page_html, pattern=PATTERN)

        return results


    def parse_reader_page(self, reader_page_html: Response, pattern: str)->list[str, str]:
        """parse the target reader page and extract the book word counts from it.

        Parameters
        ----------
        reader_page_html : Response
            the target reader page html(from `requests.get()`)
        pattern : str
            the XPath to the word counts

        Returns
        -------
        list[str, str]
            return the results including the word number and the unit.
        """        
        reader_page = reader_page_html.content.decode("utf-8")
        reader_page_node = etree.HTML(reader_page)
        results = reader_page_node.xpath(pattern)

        return results

# <--- Usage Example --->
if __name__ == "__main__":
    reader = Reader("https://weread.qq.com", "8bc329705e46708bcb0c164")
    word_count = reader.get_book_word_count()
    print(word_count)