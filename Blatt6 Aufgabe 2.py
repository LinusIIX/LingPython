dict1 = {"Harry": 3, "the": 8, "laugh": 3}
dict2 = {"Harry": 4, "the": 6, "laugh": 1}

for key in dict1:
    for key2 in dict2:
        if key == key2:
            x = dict1[key] + dict2[key2]
            print(x)
