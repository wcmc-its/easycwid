const axios = require('axios');
var aws = require('aws-sdk');
aws.config.update({ region: 'us-east-2' });

exports.handler = (event, context) => {
  //This hits the Flask api endpoint
  //***Update to match your Route53 A record that is point at Private EC2 IP.
  axios.post('http://api.dedupe-flask-app:8080/process')
    .then(response => {
      console.log("success", response.data);
    })
    .catch(error => {
      console.log("error", error);
    })
}