import re
import numpy as np
#
f = open("train4.ex", "r")

list = f.read().split(";")
print(list)
# f2 = open("scratch.txt", "r")
# list2 = f2.read().split(";")
# print(list2)
a = []
for i in list:
    a.append(i.strip())

print(a)
element = a[0]
print(re.findall(r'\[(.+)\]', element))
lst = re.split(r'\[.+\]', element)
print(lst)
inp_tar_lst = re.split("[IT]:", lst[1])
print(inp_tar_lst)

#
# def ignore_commented_lines(example_array: str):
#     while '#' in example_array:
#         a = len(example_array)
#         index = example_array.find("#")
#         find_newline = example_array[index:].find("\n") + index
#         example_array = example_array.replace(example_array[index: find_newline + 1], '\n')
#     return example_array
#
#
# lst[1] = ignore_commented_lines(lst[1])
# print(lst)
# parse_event_list(E.event[i], E.events_data[i])
# S.print_out()

# S=ExampleSet("train", "train4.ex", 1,0,1,0)
# file_str = read_in_file(S, "train4.ex")
# S.print_out()





# print(p.match("2"))011
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
