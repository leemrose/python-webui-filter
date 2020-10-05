import pandas as pd

def excelToDict(inputFile):
    df = pd.read_excel(inputFile, engine="openpyxl", header=0,
                     converters={'testcase_id':str, 'url':str, 'is_aldo_rul':str, 'filter_by':str, 'perform':str, 'menu':str, 'gender': str, 'category':str, 'item':str, 'size':str, 'colour':str, 'price':str, 'expected_filter_count':int})
    df = df.where(pd.notnull(df), None)
    df = df.dropna(how='all')
    
    row_dict = df.to_dict(orient='record')
    return row_dict