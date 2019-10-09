import * as dynamoDbLib from "../libs/dynamodb-lib";
import { success, failure } from "../libs/response-lib";

export async function main(event, context) {

  const params = {
    TableName: process.env.DYNAMODB_TABLE,
    Key:{
      'id': event['id']
    },
    UpdateExpression:"SET cwid = :c",
    ExpressionAttributeValues:{
      ':c': event["cwid"]
    },
    ReturnValues:"UPDATED_NEW"
  };

  try {
    const result = await dynamoDbLib.call("update", params);
    return success({ status: true });
  } catch (e) {
    return failure({ status: false });
  }
}
