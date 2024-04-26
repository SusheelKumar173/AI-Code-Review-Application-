# Code Analysis and Optimization Pipeline

## Overview
This repository contains the implementation of a pipeline for analyzing and optimizing code using Amazon Web Services (AWS) and Anthropic Model. The pipeline allows users to upload their code files or provide GitHub URLs, which are then processed and analyzed for debugging and optimization.Our Solution generates comprehensive code analysis reports. Leveraging AI-driven analysis, it offers actionable recommendations for enhancing code efficiency and maintainability

## Flow Description

### 1. User Interaction and File Upload
   - Users interact with the Streamlit UI to upload code files or provide a GitHub URL.

### 2. File Storage
   - Uploaded files are stored in an Amazon S3 bucket.

### 3. S3 Event Trigger
   - The upload of files to S3 triggers a Lambda function.

### 4. Lambda Function Execution
   - Lambda function is invoked with the S3 event trigger.

### 5. Debugging Prompt
   - User interaction prompts are incorporated for debugging.
   - Debugging prompts are sent to Amazon Bedrock’s Anthropic Model via API request from Lambda.

### 6. Code Analysis and Debugging
   - Anthropic Model analyzes the code and provides debugging feedback.
   - Lambda function receives debugging feedback.

### 7. Saving Debugging Results
   - Debugging results are saved to S3.

### 8. Code Review Prompt
   - Prompt for comprehensive code review and optimization feedback is sent to Anthropic Model via API request.

### 9. Code Review and Optimization
   - Anthropic Model conducts a code review and optimization analysis.
   - Lambda function receives the code review report.

### 10. Saving Code Review Results
    - Code review results are saved to S3.

### 11. Temporary Files Cleanup
    - Temporary files and directories used during processing are cleaned up.

### 12. Completion Response
    - Lambda function returns a success response indicating completion of the task.

## Credits
This project was developed by SKTS Team as part of Mavericks Designathon Program.
