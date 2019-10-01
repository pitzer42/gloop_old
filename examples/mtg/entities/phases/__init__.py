def create_indexed_list(options: list, separator='-') -> list:
    counter = 0
    indexed = list()
    for card in options:
        indexed.append(
            f'{counter}{separator}{card}'
        )
        counter += 1
    return indexed
