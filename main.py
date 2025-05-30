from Encrypt.encrypt_md5 import MD5
from API import bookid
from API import reader
from ReadFile import read
from SaveFile import save
import random
from time import sleep

TIME = 3
RETRIES = 2

def main():
    base_url = "https://weread.qq.com"
    source = './input/'
    all_target_books = ["百年孤独"]
    all_result_books_word_count = {}

    # 加载目标书籍配置，获取所有书名
    # file_reader = read.FileReader(source)
    # all_target_books = file_reader.load_books()

    for book_name in all_target_books:
        # 从API请求，得到书名的搜索结果
        for retry_count in range(RETRIES):
            book = bookid.BookInfoJSON.create(base_url, book_name)
            
            if book != None:
                break

            print("main.py retry soon...")
            delay = 2 * (retry_count + 1)
            sleep(delay)
        else:
            print("Error: skip searching the book \"{}\".".format(book_name))
            continue

        book.get_book_info_json()
        print("{}搜索完毕".format(book_name))
        book_search_result = book.parse_bookid()
        print("{}搜索结果解析完毕".format(book_name))


        for result_book_name, result_book_id in book_search_result.items():
            # 从搜索结果中，获取书名，并逐个访问Reader页面，获取字数
            # md5负责将book_id编码编码为book_reader_id
            md5 = MD5(book_id=result_book_id)
            result_book_encrypt_id = md5.encrypt_book_id_for_url()
            print("MD5编码: {} -> {}".format(result_book_id, result_book_encrypt_id))

            # 获取对应书本的字数信息
            for retry_count in range(RETRIES):
                result_book_reader = reader.Reader.create(base_url, result_book_encrypt_id)

                if result_book_reader != None:
                    break

                print("main.py retry soon...")
                delay = 2 * (retry_count + 1)
            else:
                print("Error: skip getting the book \"{}\".".format(result_book_name))
                continue

            result_book_word_count = result_book_reader.get_book_word_count()

            if result_book_word_count == None:
                print("Error: skip getting the word count of the book \"{}\".".format(result_book_name))
                continue

            all_result_books_word_count.update({result_book_name: result_book_word_count})
            print("----------------")
            print("{}\nID:{}\n字数: {}".format(result_book_name, result_book_id, result_book_word_count))
            print("----------------")

            # 道德准则，无需多言
            sleep(random.uniform(0.5, 2))   
    
    # 完成所有搜索，保存文件
    save.save_results(all_result_books_word_count)

if __name__ == "__main__":
    main()