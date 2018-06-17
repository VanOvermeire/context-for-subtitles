# Context for subtitles

This is a serverless application for automatically generating subtitles that also
show which (famous) people appear in front of the camera, for any video uploaded
to the generated S3 bucket.

### Prerequisites

- Bash, for running `setup.sh`
- AWS account
- AWS CLI installed on your pc


### Usage

You can deploy a large part of this application by running:

`./setup.sh {bucket}`

where {bucket} is the AWS S3 bucket you want your lambdas to be uploaded to.

This will generate zips for all the lambda and deploy a large part of the infrastructure.

*Not yet part of this automatic setup*:

- the S3 event to VideoAddedTopic when something is created in the /data folder
- the Step Function which is triggered by the 'stepstarter' lambda

So to make this work, you will have to set this up manually for now.

### Notes

For very large video files, you may have to increase the timeouts, which are currently
set very low (often to the default of 3, with default memory as well). Alternatively,
split up the files.

### Possible Extensions

- email lambda
- lambda to add subtitles to video
- rekognition job for (unknown) people
