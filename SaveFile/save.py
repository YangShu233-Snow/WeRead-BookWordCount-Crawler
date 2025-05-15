UNITS = ["百万", "十万", "万", "千", "百", ""]

def save_results(results: dict[str, str])-> None:
    """save results as a `YAML` file

    Parameters
    ----------
    results : dict[str, str]
        the results like dict[book_name: word_count]
    """    
    with open('output/result.yml', 'a', encoding="utf-8") as f:
        for book_name, word_count in results.items():
            word_count = transform_word_count(word_count)
            f.write("- name: \"" + book_name + "\"\n" + "  words: " + word_count + "\n")

def transform_word_count(word_count: str)->str:
    """transform word_count like "22.8 万字" to "228000"

    Parameters
    ----------
    word_count : str
        the raw word_count like "22.8 万字"

    Returns
    -------
    str
        return the transformed word_count like "228000"
    """    
    word_count = word_count.replace(" ", '').replace("字", '')
    
    for index, unit in enumerate(UNITS):
        if unit not in word_count:
            continue
        
        word_count = word_count.replace(unit, '')
        transformed_word_count = str(int(float(word_count) * 10 ** (len(UNITS) - index)))
        
        return transformed_word_count