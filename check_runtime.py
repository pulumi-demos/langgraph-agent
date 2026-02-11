import boto3
import subprocess

# Get runtime ID from Pulumi output
runtime_id = subprocess.check_output(["pulumi", "stack", "output", "agent_runtime_id"], text=True).strip()

client = boto3.client('bedrock-agentcore-control', region_name='us-east-1')

try:
    response = client.get_agent_runtime(agentRuntimeId=runtime_id)
    
    print("✅ Agent runtime retrieved successfully!")
    print(f"\nRuntime Details:")
    print(f"  Name: {response['agentRuntimeName']}")
    print(f"  ID: {response['agentRuntimeId']}")
    print(f"  ARN: {response['agentRuntimeArn']}")
    print(f"  Status: {response['status']}")
    print(f"  Created: {response.get('createdAt', 'N/A')}")
    print(f"  Updated: {response.get('lastUpdatedAt', 'N/A')}")
    print(f"  Role ARN: {response.get('roleArn', 'N/A')}")
    
    if response['status'] == 'READY':
        print("\n✅ Runtime is READY and operational!")
    else:
        print(f"\n⚠️  Runtime status: {response['status']}")
        if 'failureReason' in response:
            print(f"  Failure reason: {response['failureReason']}")
    
except Exception as e:
    print(f"❌ Error checking agent runtime: {e}")
