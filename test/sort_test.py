import time
import pandas as pd

df = pd.read_csv('data.csv', index_col = 0)
lists = df.values.tolist()
#print(lists)
index_lists = [] + df.reset_index().values.tolist()
def select_element(subarray, element_index):
    return subarray[element_index]


def return_only_indexes(list):
    return [subarray[0] for subarray in list]

def return_sorted_only_indexes(list, column, reverse):
    return [subarray[0] for subarray in return_sorted_with_indexes(list, column, reverse)]

def return_full_to_sorted_with_indexes(list, column, reverse):
    return return_only_indexes(return_sorted_with_indexes(list, column, reverse))
###################################
def return_one_column_with_indexes(list, desired_element_index):
    return [[index, select_element(subarray, desired_element_index)] for index, subarray in enumerate(list)]
def return_sorted_with_indexes(list, column, reverse):
    return sorted(list, key=lambda x:x[column], reverse=reverse)
def return_only_indexes(list):
    return [subarray[0] for subarray in list]

def return_full_to_one_to_sorted_with_indexes(list, column, reverse):
    return return_only_indexes(return_sorted_with_indexes(return_one_column_with_indexes(list, desired_element_index), column, reverse))

'''
column = 2
test = return_only_indexes(return_sorted_with_indexes(index_lists, desired_element_index + 1, reverse))
print(test)
column = 1
test = return_only_indexes(return_sorted_with_indexes(return_one_column_with_indexes(lists, desired_element_index), column, reverse))
print(test)

start_time = time.time()
index_lists = [] + df.reset_index().values.tolist()
test = return_only_indexes(return_sorted_with_indexes(index_lists, desired_element_index + 1, reverse))
end_time = time.time()
execution_time = end_time - start_time
print(execution_time)
'''
start_time = time.time()
lists = df.values.tolist()
test = return_only_indexes(return_sorted_with_indexes(return_one_column_with_indexes(lists, 2), 1, 0))
print(test)
end_time = time.time()
execution_time = end_time - start_time
print(execution_time)


start_time = time.time()

end_time = time.time()
execution_time = end_time - start_time
print(execution_time)
