import pandas as pd
from boto3.dynamodb.types import TypeSerializer
import json

def replaceObjectName(data):
    data = data.replace('"M"', '"m"')
    data = data.replace('"L"', '"l"')
    data = data.replace('"S"', '"s"')
    data = data.replace('"N"', '"n"')
    return data

def converterToDynamodbFormat(data):
    typer = TypeSerializer()
    dynamodbJsonData = json.dumps(typer.serialize(data)['M'])
    return replaceObjectName(dynamodbJsonData)

df1 = pd.read_csv('output.csv')
df = df1.astype(str)
record_number, columns_number = df.shape
print(df.shape)

records = []
for record_index in range(record_number):
    record = {}
    for columns_index in range(columns_number):
        column_name = df.columns[columns_index]
        record[column_name] = df[column_name][record_index]
    records.append(record)

count = 0
with open("output.txt", 'w+') as f:
    for record in records:
        count += 1
        f.write(converterToDynamodbFormat(record))
        f.write('\n')
print(count)
