import re
import numpy as np

f = open("train4.ex", "r")

list = f.read().split(";")
a = []
for i in list:
    a.append(i.strip())

print(a)
element = a[0]
print(re.findall(r'\[(.+)\]', element))
print(re.split(r'\[.+\]', element))
# if "defT:" in element:
#     index = element.find("defT:")
#     find_newline = element[index:].find("\n")
#     x = element[index + len("defT:"): index + find_newline]
#     print(x)
# print(element)
# p = re.compile("(^|\\n)[0-9]+(\\n|$)")
# m = p.search(element)
# print(m)
# print(element[m.start() + 1: m.end()])
# if m is not None:
#     start = m.start()
#     end = m.end()
#     print(element[start: end])
# list.pop()
# print(list)
# print((list[1]).strip("\n"))

# for i in range(len(list)):
#     inp_tar_lst =re.split("[A-Z]:", list[i])
#     inp_tar_lst.pop(0)
#     print(inp_tar_lst[0].split())
#
#     event_dict = {"I": inp_tar_lst[0].split(), "T": inp_tar_lst[1].split()}
#     print(event_dict)

# a = np.array([2, 23])
# print(a)
# a = np.append(a, [])
# a = np.append(a, [2])
# print(a[1])
# print(a)
# print(a.size)
# print(a.reshape((5, 2)))
# b = np.zeros((5, 5))
# print(b)
