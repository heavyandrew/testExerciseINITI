import uvicorn

import pandas as pd
from fastapi import FastAPI, HTTPException

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

def indexing_(data):
    result = []
    for i in range(len(data[0])):
        result.append(return_full_to_one_to_sorted_with_indexes(data, i, 0))
    return result


class Server():
    def __init__(self, port, data_path):
        self.port = port
        #Здесь библиотека используется только для чтения из файла csv
        df = pd.read_csv(data_path, index_col=0)
        #здесь dataframe переводится в двумерный массив
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

        @self.app.post("/add")
        def add(place: int, name: str, age: int, heights: int, foot: int, english: str):
            in_data = [place, name, age, heights, foot, english]
            if place < len(self.data):
                self.data.insert(place, in_data)
            else:
                self.data.append(in_data)
            self.indexing()
        @self.app.delete("/delete")
        def delete(place: int):
            if place < len(self.data):
                self.data.pop(place)
                self.indexing()
            else:
                raise HTTPException(status_code=400, detail="No such item")

        @self.app.post("/update")
        def update(place: int, name: str, age: int, heights: int, foot: int, english: str):
            if place < len(self.data):
                self.data[place] = [place, name, age, heights, foot, english]
                self.indexing()
            else:
                raise HTTPException(status_code=400, detail="No such item")
    def indexing(self):
        result = indexing_(self.data)
        self.indexes = result.copy()
    def run(self):
        uvicorn.run(self.app, host='0.0.0.0', port=int(self.port))