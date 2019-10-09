import AWS from "aws-sdk";

var options = { region: 'us-east-2' }
AWS.config.update(options);

export function call(action, params) {
  const dynamoDb = new AWS.DynamoDB.DocumentClient();
  return dynamoDb[action](params).promise();
}
