
def uniquelines():
    file_to_unique = open('temp_file_for_replace.txt', 'r+', encoding='utf-8')
    filelines = file_to_unique.readlines()
    file_to_unique.close()
    file_with_unique = open("wordlist_unique.txt", "w", encoding='utf-8')
    unique = {}
    result = []
    for item in filelines:
        if item.strip() in unique:
            continue
        unique[item.strip()] = 1
        result.append(item)
    file_with_unique.writelines(result)
    file_with_unique.close()


# def uniquelines(lineslist):
#     unique = {}
#     result = []
#     for item in lineslist:
#         if item.strip() in unique:
#             continue
#         unique[item.strip()] = 1
#         result.append(item)
#     return result


# file_to_unique = open('temp_file_for_replace.txt', 'r+', encoding='utf-8')
# filelines = file_to_unique.readlines()
# file_to_unique.close()
# file_with_unique = open("wordlist_unique.txt", "w", encoding='utf-8')
# file_with_unique.writelines(uniquelines(filelines))
# file_with_unique.close()
