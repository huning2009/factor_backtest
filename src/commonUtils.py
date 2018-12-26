#coding:utf-8
import pandas as pd
import numpy as np


# 一次性读取内存会爆掉 使用分块读取
def readFile(path):
    f = open(path)
    reader = pd.read_csv(f, sep=',', iterator=True)
    loop = True
    chunkSize = 100000
    chunks = []
    while loop:
        try:
            chunk = reader.get_chunk(chunkSize)
            chunks.append(chunk)
        except StopIteration:
            loop = False
            print("Iteration is stopped.")
    df = pd.concat(chunks, ignore_index=True)
    return df
