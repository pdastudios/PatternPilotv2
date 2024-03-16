num_list = [13,12,14,13,15,10,9,9,9,13]

for i in num_list:
    if i%3 != 0:
        num_list.remove(i)

print(num_list)
