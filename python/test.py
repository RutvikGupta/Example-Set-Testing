import re
f = open("scratch.txt", "r")

list = f.read().split(";")
list.pop(0)
list.pop()
# print(list)
# print((list[1]).strip("\n"))

for i in range(len(list)):
    inp_tar_lst =re.split("[A-Z]:", list[i])
    inp_tar_lst.pop(0)
    print(inp_tar_lst[0].split())

    event_dict = {"I": inp_tar_lst[0].split(), "T": inp_tar_lst[1].split()}
    print(event_dict)
