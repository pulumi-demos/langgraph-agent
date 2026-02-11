import boto3
import json
import uuid
import subprocess

# Get runtime ARN from Pulumi output
runtime_arn = subprocess.check_output(["pulumi", "stack", "output", "agent_runtime_arn"], text=True).strip()

client = boto3.client('bedrock-agentcore', region_name='us-east-1')

try:
    response = client.invoke_agent_runtime(
        agentRuntimeArn=runtime_arn,
        qualifier='DEFAULT',
        traceId=str(uuid.uuid4()),
        contentType='application/json',
        payload=json.dumps({
            "prompt": "Hello, can you help me?"
        })
    )
    
    print("✅ Agent runtime invoked successfully!")
    print(f"Response status: {response['ResponseMetadata']['HTTPStatusCode']}")
    print(f"Content type: {response.get('contentType', 'N/A')}")
    
    # Read the streaming response
    if 'payload' in response:
        payload_data = response['payload'].read()
        print(f"Payload size: {len(payload_data)} bytes")
        if payload_data:
            print(f"Response preview: {payload_data[:200]}")
    
except Exception as e:
    print(f"❌ Error invoking agent runtime: {e}")
