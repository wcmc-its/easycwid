#### Usage

To use this repo locally you need to have the [Serverless framework](https://serverless.com) installed.

``` bash
$ npm install serverless -g
```

Clone this repo and install the NPM packages.

``` bash
$ git clone git repo
$ yarn install
```

Run a single API on local.

``` bash
$ serverless invoke local --function list --path event.json
```

Finally, run this to deploy to your AWS account.
If multiple AWS configs, use profiles and update below to your alias

## deploy all
AWS_PROFILE=plg serverless deploy

## deploy all by stage
AWS_PROFILE=plg serverless deploy --stage dev --region us-east-2

## deploy function only
serverless deploy function --function myFunctionName
example
AWS_PROFILE=plg serverless deploy function --function myFunctionName --stage dev --region us-east-2

## Testing locally
AWS_PROFILE=plg serverless invoke local --function create --path mocks/create-event.json
AWS_PROFILE=plg serverless invoke local --function get --path mocks/get-event.json
AWS_PROFILE=plg serverless invoke local --function update --path mocks/update-event.json

## Testing live
AWS_PROFILE=plg serverless invoke --function create --path mocks/create-event.json
AWS_PROFILE=plg serverless invoke --function list --stage dev --path mocks/list-event.json-2
AWS_PROFILE=plg serverless invoke --function list_by_cwid --stage dev --path mocks/list-by-cwid-event.json