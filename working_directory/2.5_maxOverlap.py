from itertools import groupby

with open("fullList_file.txt", 'r') as f:
    fullList = [line.rstrip('\n') for line in f]
    
#def most_common(lst):
#    return max(set(lst), key=lst.count)    

#fullList.sort()
#print(most_common(fullList))
#freq = [len(list(group)) for key, group in groupby(fullList)]
#print(max(freq))



from collections import Counter
fullList_str = [str(i) for i in fullList]
most_common_words_count= [word_count for word, word_count in Counter(fullList_str).most_common(8)]
most_common_words_words= [word for word, word_count in Counter(fullList_str).most_common(8)]
print(most_common_words_count)
print(most_common_words_words)

#c = Counter(words_to_count)
#print(c.most_common(3))
