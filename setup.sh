#!/usr/bin/env bash

LAMBDAS=("checker" "combiner" "rekognitionjob" "stepstarter" "transcribejob") # names of the directories which contain the lambdas
LAMBDA_FOLDER="lambda-zips/"  # folder to place the zips in, can be changed
SAM_YAML="sam-infra.yaml"
SAM_STACK_NAME="subtitles-with-context-stack" # default name for stack, can be changed

# gather requirements and upload zip; folders should be given as args
function handle_lambda {
    folder=$1
    zip_name=${folder}.zip

    cd ${folder}

    cp -rf ../helpers .

    zip -r ${zip_name} . >> /dev/null

    echo "Uploading zip $zip_name to S3"
    aws s3 cp ${zip_name} "s3://${BUCKET}/$LAMBDA_FOLDER" >> /dev/null

    # cleanup
    rm -rf helpers
    rm -f ${zip_name}

    cd ..
}

if [ $# -lt 1 ]; then
    echo "Needs a bucket!"
    echo "Usage ./setup.sh <bucket>"
    exit 1
fi

BUCKET=$1

for folder in "${LAMBDAS[@]}"
do
    handle_lambda ${folder}
done

cd infra

echo "Deploying stack"
aws cloudformation deploy \
    --template-file ${SAM_YAML} \
    --stack-name ${SAM_STACK_NAME} \
    --capabilities CAPABILITY_IAM
