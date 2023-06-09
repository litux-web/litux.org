type: article
title: CloudWatch notifications via IFTTT
last-updated: 2023-06-08

Create a new Lambda function
https://eu-central-1.console.aws.amazon.com/lambda/home?region=eu-central-1#/create/function

Author from Scratch
Function name: SNS-to-IFTTT
Runtime: Node.js 18.x
Architecture: arm64 (or x86_64)

On "Configuration", "Environment variables", add
iftttMakerEventName
iftttMakerSecretKey

On "Code source" rename `index.mjs` into `index.js` and paste
```
var https = require('https');
var querystring = require("querystring");

// IFTTT Maker Webhooks configuration, see https://ifttt.com/maker_webhooks
var iftttMakerEventName = process.env.iftttMakerEventName;
var iftttMakerSecretKey = process.env.iftttMakerSecretKey;

var iftttMakerUrl =
    'https://maker.ifttt.com/trigger/'
    + iftttMakerEventName
    + '/with/key/'
    + iftttMakerSecretKey;

exports.handler = function(event, context) {
    var subject = "";
    var message = "";
    if (event.Records) {
        subject = event.Records[0].Sns.Subject;
        message = event.Records[0].Sns.Message;
    }
    if (!subject) {
        return;
    }

    var params = querystring.stringify({value1: subject, value2: message});
    var iftttMakerUrlWithParams = encodeURI(iftttMakerUrl) + '?' + params
    https.get(iftttMakerUrlWithParams, function(res) {
        console.log("Got response: " + res.statusCode);
        res.setEncoding('utf8');
        res.on('data', function(d) {
            console.log('Body: ' + d);
        });
        context.succeed(res.statusCode);
    }).on('error', function(e) {
        console.log("Got error: " + e.message);
        context.fail(e.message);
    });

};
```

Click Deploy

Click Test and configure a Test event
```
{
  "Records": [
    {
      "Sns": {
        "Subject": "test subject",
        "Message": "test message"
      }
    }
  ]
}
```

Click Test again to test the result
```
Test Event Name
TestEvent

Response
200

Function Logs
START RequestId: 9fda9485-d13f-4b36-b2ef-65954ad406c8 Version: $LATEST
2023-06-08T16:35:25.066Z	9fda9485-d13f-4b36-b2ef-65954ad406c8	INFO	Event:  { Records: [ { Sns: [Object] } ] }
2023-06-08T16:35:25.107Z	9fda9485-d13f-4b36-b2ef-65954ad406c8	INFO	Event Records:  [ { Sns: { Subject: 'test subject', Message: 'test message' } } ]
2023-06-08T16:35:25.107Z	9fda9485-d13f-4b36-b2ef-65954ad406c8	INFO	From SNS subject:  test subject
2023-06-08T16:35:25.107Z	9fda9485-d13f-4b36-b2ef-65954ad406c8	INFO	From SNS message:  test message
2023-06-08T16:35:25.551Z	9fda9485-d13f-4b36-b2ef-65954ad406c8	INFO	Got response: 200
2023-06-08T16:35:25.567Z	9fda9485-d13f-4b36-b2ef-65954ad406c8	INFO	Body: Congratulations! You've fired the litux event
END RequestId: 9fda9485-d13f-4b36-b2ef-65954ad406c8
REPORT RequestId: 9fda9485-d13f-4b36-b2ef-65954ad406c8	Duration: 564.42 ms	Billed Duration: 565 ms	Memory Size: 128 MB	Max Memory Used: 68 MB	Init Duration: 177.99 ms

Request ID
9fda9485-d13f-4b36-b2ef-65954ad406c8
```

## SNS

Go to SNS and create a new Topic
Type: Standard
Name: IFTTT

Go back to Lambda `SNS-to-IFTTT` and add a Triger and set it to `SNS` and SNS Topic `IFTTT`.

Go to CloudWatch and set an alarm
Select "Select an existing SNS topic" and "Send a notification to..." select `IFTTT` and ignore the mentions to email.

