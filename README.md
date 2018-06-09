# Context for subtitles

...

### Usage

You can generate the lambda zips of this project and upload them to S3 
automatically by running the following command from the root of this project:

`./setup.sh {bucket}`

where {bucket} is the AWS S3 bucket you want your lambdas to be uploaded to.

### TODO's

- add SAM yaml to automatically provision infrastructure

### Possible Extensions

- email lambda
- lambda to add subtitles to video
- rekognition job for (unknown) people
