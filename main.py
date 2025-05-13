from MD5 import encrypt_md5
from API import bookid
from API import reader

if __name__ == "__main__":
    info = bookid.BookInfoJSON("https://weread.qq.com/", "百年孤独")
    result = info.get_book_info_json()