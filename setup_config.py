#!/usr/bin/env python3
"""Helper script to fetch CloudFormation stack outputs and update Pulumi config"""
import json
import subprocess
import sys

def get_cfn_outputs(stack_name):
    """Fetch CloudFormation stack outputs"""
    try:
        result = subprocess.run(
            ["aws", "cloudformation", "describe-stacks", "--stack-name", stack_name],
            capture_output=True,
            text=True,
            check=True
        )
        stacks = json.loads(result.stdout)
        outputs = {}
        for output in stacks["Stacks"][0].get("Outputs", []):
            outputs[output["OutputKey"]] = output["OutputValue"]
        return outputs
    except subprocess.CalledProcessError as e:
        print(f"Error fetching stack outputs: {e.stderr}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

def update_pulumi_config(outputs):
    """Update Pulumi configuration with CloudFormation outputs"""
    config_map = {
        "ProductInfo1stKnowledgeBaseId": outputs.get("ProductInfo1stKnowledgeBaseId"),
        "PetCare2ndKnowledgeBaseId": outputs.get("PetCare2ndKnowledgeBaseId"),
        "SolutionAccessRoleArn": outputs.get("SolutionAccessRoleArn"),
        "PetStoreInventoryManagement1stFunction": outputs.get("PetStoreInventoryManagement1stFunction"),
        "PetStoreUserManagement2ndFunction": outputs.get("PetStoreUserManagement2ndFunction"),
        "PetStoreGuardrailId": outputs.get("PetStoreGuardrailId"),
        "PetStoreGuardrailVersion": outputs.get("PetStoreGuardrailVersion", "1")
    }
    
    # Set Pulumi config
    config_json = json.dumps(config_map)
    try:
        subprocess.run(
            ["pulumi", "config", "set", "knowledgeBaseStackOutputs", config_json, "--plaintext"],
            check=True
        )
        print("✓ Pulumi configuration updated successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error updating Pulumi config: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python setup_config.py <cloudformation-stack-name>")
        sys.exit(1)
    
    stack_name = sys.argv[1]
    print(f"Fetching outputs from CloudFormation stack: {stack_name}")
    
    outputs = get_cfn_outputs(stack_name)
    if outputs:
        print(f"Found {len(outputs)} outputs")
        if update_pulumi_config(outputs):
            print("\n✓ Configuration complete! Run 'pulumi up' to deploy.")
        else:
            sys.exit(1)
    else:
        print("Failed to fetch CloudFormation outputs")
        sys.exit(1)
