import os

class FileReader:
    def __init__(self, source: str):
        self.source = source

    def load_books(self)->list[str]:
        """load all books

        Returns
        -------
        list[str]
            return a list like `list[config_file_path]`
        """        
        source_file_path = self.load_search_book()
        all_books = self.read_file(source_file_path)

        return all_books

    def load_search_book(self)->list[str]:
        """load target book names in the config files

        Returns
        -------
        list[str]
            return a list like `list[config_file_path]`
        """         
        source_file_paths = []
        
        for root, _, filenames in os.walk(self.source, topdown=True):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                source_file_paths.append(file_path)
        
        return source_file_paths

    def read_file(self, source_file_paths: list[str])->list[str]:
        """read file and load all target books

        Parameters
        ----------
        source_file_paths : list[str]
            the config file paths

        Returns
        -------
        list[str]
            return the name of all books like `list[book_name]`
        """        
        all_books = []
        
        for file_path in source_file_paths:
            with open(file_path, "r") as f:
                data = f.readlines()
            
            for book_name in data:
                if '\n' in book_name:
                    book_name = book_name.replace('\n', '')
                
                all_books.append(book_name)

        return all_books

# <--- Usage Example --->
if __name__ == "__main__":
    source_file_paths = "../input/"
    file_reader = FileReader(source_file_paths)
    all_books = file_reader.load_books()

    for book in all_books:
        print(book)