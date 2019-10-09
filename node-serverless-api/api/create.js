import uuid from "uuid";
import * as dynamoDbLib from "../libs/dynamodb-lib";
import { success, failure } from "../libs/response-lib";

export async function main(event, context) {
  const data = JSON.parse(event.body)
  let params = {
    TableName: process.env.DYNAMODB_TABLE,
    Item: {
    
      "id": uuid.v1(),
      "title": data.title,
      "source": data.source,
      "status": data.status,
      "cwid": data.cwid,
      "surname": data.surname,
      "middleName": data.middleName,
      "givenName": data.givenName,
      "prefix": data.prefix,
      "suffix": data.suffix,
      "npi": data.npi,
      "email": data.email,
      "monthOfBirth": data.monthOfBirth,
      "dayOfBirth": data.dayOfBirth,
      "genderScore": data.genderScore,
      "departmentLabel": data.departmentLabel,
      "modifyTimestamp": data.modifyTimestamp,
      "location": data.location,
      "postalCode": data.postalCode,
      "startDate": data.startDate,
      "createdAt": Date.now().toString(),
      "sorId": data.sorId,
      "cluster id": data["cluster id"],
      "confidence": data.confidence
    }
 };

  try {
    await dynamoDbLib.call("put", params);
    return success(params.Item);
  } catch (e) {
    return failure( e );
  }
}
