from flask import Flask, url_for, request, jsonify
import pandas as pd
import pandas_dedupe
import pandas_dedupe_custom.dedupe_dataframe as dedupe_dataframe
import boto3
from celery import Celery

app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

df_table = pd.DataFrame()

@celery.task(bind=True)
def run_dedupe(self):
  TableName = 'dev-cwid-records'
  dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
  table = dynamodb.Table(TableName)
  response = table.scan()
  data = response['Items']

  while response.get('LastEvaluatedKey', False):
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    data.extend(response['Items'])
  print("db scan finished")

  df_table = pd.DataFrame.from_dict(data, orient='columns')

  #Make sure column names match headers in DynamoDB
  df_result = dedupe_dataframe.dedupe_dataframe(df_table, [
      ('givenName', 'String', 'has missing'),
      ('surname', 'String', 'has missing'),
      ('middleName', 'String', 'has missing'),
      ('monthOfBirth', 'Exact', 'has missing'),
      ('dayOfBirth', 'Exact', 'has missing'),
      ('source', 'Exact', 'has missing'),
      ('title', 'String', 'has missing'),
      ('departmentLabel', 'String', 'has missing')], canonicalize=False, config_name="dedupe_dataframe")

  #Transform the pandas dataframe to a data dictionary
  transformed_df = df_result.T.to_dict().values()
  print("starting db updates", df_result.shape)
  count = 0
  # Put the updated items into the table
  for record in transformed_df:
      count += 1
      table.update_item(
          Key={
              'id': record['id']
          },
          UpdateExpression="SET confidence = :co, #clusterId = :cl",
          ExpressionAttributeValues={
              ':co': record["confidence"],
              ':cl': record["cluster id"]
          },
          ExpressionAttributeNames={
              '#clusterId': 'cluster id'
          },
          ReturnValues="UPDATED_NEW"
      )

  print("done db updates:", count)
  return jsonify({'status': 201, 'recordsUpdated': count})

@app.route('/process', methods=['POST'])
def process():
  task = run_dedupe.apply_async()
  return jsonify({'status': 201, 'status': 'process started'})

if __name__ == '__main__':
  app.run()