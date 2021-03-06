import * as dynamoDbLib from "../libs/dynamodb-lib";
import { success, failure } from "../libs/response-lib";

export async function main(event, context) {

  const params = {
    TableName: process.env.DYNAMODB_TABLE,
    IndexName: 'cluster-id-index', // maps back to the serverless config variable above
    KeyConditionExpression: "#clusterId=:cl",
    ExpressionAttributeValues: { ":cl": event.pathParameters.clusterId },
    ExpressionAttributeNames: {
      '#clusterId': 'cluster id'
    }
  };

  try {
    const result = await dynamoDbLib.call("query", params);
    // Return the matching list of items in response body
    return success(result.Items);


  } catch (e) {
    return failure({ error: JSON.stringify(e.message) });
  }
}
