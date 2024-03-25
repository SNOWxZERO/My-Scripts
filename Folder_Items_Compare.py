import os

lost = []
path1 = 'F:\Anime'
path2 = 'J:\Anime'
list1 = os.listdir(path1)
list2 = os.listdir(path2)
diffrences = list(set(list1) - set(list2))

print('\n'.join(sorted(list1)))
