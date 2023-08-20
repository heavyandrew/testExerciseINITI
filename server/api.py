import uvicorn
import asyncio
import time

import pandas as pd
from fastapi import FastAPI

def select_element(subarray, element_index):
    return subarray[element_index]
def return_one_column_with_indexes(list, desired_element_index):
    return [[index, select_element(subarray, desired_element_index)] for index, subarray in enumerate(list)]
def return_sorted_with_indexes(list, column, reverse):
    return sorted(list, key=lambda x:x[column], reverse=reverse)
def return_only_indexes(list):
    return [subarray[0] for subarray in list]

def return_full_to_one_to_sorted_with_indexes(list, column, reverse):
    return return_only_indexes(return_sorted_with_indexes(return_one_column_with_indexes(list, column), 1, reverse))

class Server():
    def __init__(self, port, data_path):
        self.port = port
        df = pd.read_csv(data_path, index_col=0)
        self.data = df.values.tolist()
        self.app = FastAPI()
        #self.indexes = [[index for index in range(len(self.data))]]
        self.indexes = []
        self.indexing()

        @self.app.get("/get")
        def get(cursor: int, lines: int, column: int, reverse: bool):
            #start_time = time.time()
            response = []
            if reverse == False:
                for i in range(cursor, cursor + lines):
                    response.append(self.data[self.indexes[column][i]])
            else:
                for i in range(cursor, cursor + lines):
                    reversed1 = self.indexes[column][::-1]
                    response.append(self.data[reversed1[i]])
            #end_time = time.time()
            #execution_time = end_time - start_time
            #print(execution_time)
            return response

        @self.app.get("/getlist")
        def get(cursor: int, lines: int, column: int, reverse: bool):
            # start_time = time.time()
            response = []
            if reverse == False:
                for i in range(cursor, cursor + lines):
                    response.append(self.data[self.indexes[column][i]])
            else:
                for i in range(cursor, cursor + lines):
                    reversed1 = self.indexes[column][::-1]
                    response.append(self.data[reversed1[i]])
            # end_time = time.time()
            # execution_time = end_time - start_time
            # print(execution_time)
            return {'id_list': response}
    def indexing(self):
        for i in range(len(self.data[0])):
            self.indexes.append(return_full_to_one_to_sorted_with_indexes(self.data, i, 0))
    def run(self):
        uvicorn.run(self.app, host='0.0.0.0', port=int(self.port))