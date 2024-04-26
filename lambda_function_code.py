import boto3
import os
import json
import tempfile

s3_client = boto3.client('s3')

def download_file_from_s3(bucket_name, file_key):
    """
    Download a file from S3 to a temporary directory.
    
    Args:
    - bucket_name: The name of the S3 bucket.
    - file_key: The key of the file to download.
    
    Returns:
    - The path to the downloaded file.
    """
    temp_dir = tempfile.mkdtemp()
    download_path = os.path.join(temp_dir, file_key.split('/')[-1])
    s3_client.download_file(bucket_name, file_key, download_path)
    return download_path

def invoke_model_and_upload_result(client, model_id, input_data, bucket_name, result_key):
    """
    Invoke an Anthropic model with input data and upload the result to S3.
    
    Args:
    - client: The boto3 client for invoking the model.
    - model_id: The ID of the Anthropic model.
    - input_data: The input data for the model.
    - bucket_name: The name of the S3 bucket to upload the result.
    - result_key: The key for the result file in the S3 bucket.
    """
    input_data_json = json.dumps(input_data)
    response = client.invoke_model(contentType='application/json', body=input_data_json, modelId=model_id)
    inference_result = response['body'].read().decode('utf-8')
    data = json.loads(inference_result)
    content_text = data['content'][0]['text']
    s3_client.put_object(Bucket=bucket_name, Key=result_key, Body=content_text)
    print("Anthropic model results saved to S3")

def lambda_handler(event, context):
    # Extracting information from the S3 event trigger
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    download_path = download_file_from_s3(bucket_name, file_key)
    
    with open(download_path, 'r') as file:
        code_content = file.read()
        print("Code content:", code_content)
    
    # Debugging prompt
    prompt1 = code_content + "\nDebug the above code, and also provide me the corrected code if any issues/bugs found. If no bugs found, test it with few test data.Provide me the total number of errors found"
    
    print("======================")
    print("Prompt1 : ")
    print(prompt1)
    
    model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
    
    input_data_debug = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt1
                    }
                ]
            }
        ],
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 20000
    }

    debug_result_key = "results/DebuggedCode.txt"
    
    invoke_model_and_upload_result(boto3.client('bedrock', region_name='us-east-1', endpoint_url='https://bedrock-runtime.us-east-1.amazonaws.com'), model_id, input_data_debug, bucket_name, debug_result_key)
    
    print("===============================================================")
    
    print("Prompt2")
    
    # Review prompt
    prompt2 = code_content + "\nGenerate comprehensive code review and optimization feedback report for the provided code. This includes 1) evaluating static code analysis, 2)adherence to coding standards, 3)implementation of best practices, 4) identification of duplicate/redundant code, 5)assessment of code quality and 6)suggestions for improvement. Also provide percentage criteria for each along with improvements to reach 100%."
    

    print(prompt2)
    # Input data for review
    input_data_review = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt2
                    }
                ]
            }
        ],
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 20000
    }

    review_result_key = "results/Report.txt"
    
    invoke_model_and_upload_result(boto3.client('bedrock', region_name='us-east-1', endpoint_url='https://bedrock-runtime.us-east-1.amazonaws.com'), model_id, input_data_review, bucket_name, review_result_key)
    
    os.remove(download_path)
    os.rmdir(os.path.dirname(download_path))

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
