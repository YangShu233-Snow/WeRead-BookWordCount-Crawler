from Encrypt.encrypt_md5 import MD5
from API import bookid
from API import reader
from ReadFile import read
import random
from time import sleep

def main():
    base_url = "https://weread.qq.com"
    source = './Input/'
    units = ["百万", "十万", "万", "千", "百", ""]
    all_target_books = ["百年孤独"]
    all_result_books_word_count = {}

    # 加载目标书籍配置，获取所有书名
    file_reader = read.FileReader(source)
    all_target_books = file_reader.load_books()

    for book_name in all_target_books:
        # 从API请求，得到书名的搜索结果
        book = bookid.BookInfoJSON(base_url, book_name)
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
            result_book_reader = reader.Reader(base_url, result_book_encrypt_id)
            result_book_word_count = result_book_reader.get_book_word_count()
            
            if "error" in result_book_word_count:
                print(result_book_word_count + ": {}".format(result_book_name))
                continue

            all_result_books_word_count.update({result_book_name: result_book_word_count})
            print("----------------")
            print("{}\nID:{}\n字数: {}".format(result_book_name, result_book_id, result_book_word_count))
            print("----------------")

            # 道德准则，无需多言
            sleep(random.uniform(0.5, 2))

    with open('result.txt', 'a', encoding="utf-8") as f:
        for key, value in all_result_books_word_count.items():
            value: str = value.replace(" ", '').replace("字", '')
            for index in range(len(units)):
                if units[index] not in value:
                    continue

                value = value.replace(units[index], '')
                value = str(int(float(value) * 10 ** (len(units) - index)))
                break

            f.write("- name: \"" + key + "\"\n" + "  words: " + value + "\n")

if __name__ == "__main__":
    main()