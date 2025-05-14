from Encrypt.encrypt_md5 import MD5
from API import bookid
from API import reader

def main():
    base_url = "https://weread.qq.com"
    all_target_books = ["百年孤独"]
    all_result_books_word_count = {}

    for book_name in all_target_books:
        book = bookid.BookInfoJSON(base_url, book_name)
        book.get_book_info_json()
        book_search_result = book.parse_bookid()

        for result_book_name, result_book_id in book_search_result.items():
            md5 = MD5(book_id=result_book_id)
            result_book_encrypt_id = md5.encrypt_book_id_for_url()
            result_book_reader = reader.Reader(base_url, result_book_encrypt_id)
            result_book_word_count = result_book_reader.get_book_word_count()
            all_result_books_word_count.update({result_book_name: result_book_word_count})

    for key, value in all_result_books_word_count.items():
        print("{}: {}".format(key, value))

if __name__ == "__main__":
    main()