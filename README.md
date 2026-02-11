# LangGraph ReAct Agent on AWS Bedrock AgentCore - Pulumi Infrastructure

## Overview

This Pulumi program provisions production-ready infrastructure for deploying a LangGraph ReAct agent to AWS Bedrock AgentCore. It creates all necessary AWS resources using infrastructure as code, including Knowledge Bases, Lambda functions, and containerized agent runtime.

## Getting Started

### Prerequisites

- AWS CLI configured with appropriate credentials
- Docker installed and running
- Pulumi CLI installed
- Python 3.12+
- UV package manager ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))

### Setup

1. **Deploy CloudFormation stack** (Knowledge Bases, Lambdas, Guardrails):
   ```bash
   aws cloudformation create-stack \
     --stack-name pet-store-kb \
     --template-body file://pet_store_knowledge_bases.yaml \
     --capabilities CAPABILITY_IAM
   ```

2. **Sync Knowledge Bases**:
   - Navigate to AWS Console → Bedrock → Knowledge Bases
   - Sync both Product Info and Pet Care knowledge bases

3. **Install dependencies**:
   ```bash
   uv sync
   ```

4. **Configure Pulumi with CloudFormation outputs**:
   ```bash
   uv run python setup_config.py pet-store-kb
   ```

5. **Login to Pulumi** (if needed):
   ```bash
   pulumi login
   ```

6. **Preview infrastructure**:
   ```bash
   pulumi preview
   ```

7. **Deploy infrastructure**:
   ```bash
   pulumi up
   ```

## Architecture

The infrastructure includes:

### Core Components

- **AWS Bedrock AgentCore Runtime**: Containerized execution environment for the LangGraph agent
- **ECR Repository**: Stores the ARM64 Docker image for the agent
- **Knowledge Bases (2)**:
  - Product Information KB
  - Pet Care KB
- **Lambda Functions (2)**:
  - Inventory Management System
  - User Management System
- **Guardrails**: Content filtering and safety controls
- **IAM Roles & Policies**: Secure access control for all components

### Key Features

- **ARM64 Architecture**: Optimized for AWS Graviton processors
- **OpenTelemetry Integration**: Full observability with CloudWatch GenAI dashboard
- **Automated Docker Build**: Uses Pulumi Docker Build provider for image building
- **Production Security**: Proper IAM roles, policies, and guardrails
- **UV Package Manager**: Fast, reliable dependency management

## Resources Created

1. **ECR Repository**: Container image storage with lifecycle policy
2. **Docker Image**: LangGraph agent with OpenTelemetry instrumentation
3. **AgentCore Runtime**: Serverless runtime integrated with Knowledge Bases, Lambda, and Guardrails
4. **Configuration**: Pulumi stack configuration from CloudFormation outputs

## Deployment

### Prerequisites

- CloudFormation stack deployed and Knowledge Bases synced
- AWS CLI configured with appropriate credentials
- Docker installed and running
- Pulumi CLI installed
- UV package manager (already configured)

### Deploy

```bash
# Preview changes
pulumi preview

# Deploy infrastructure
pulumi up

# Get outputs
pulumi stack output
```

### Key Outputs

- `agent_runtime_arn`: Full ARN for agent invocation
- `agent_runtime_name`: Runtime name for evaluation
- `ecr_repository_url`: Container image repository

## Agent Capabilities

The deployed agent handles:

- **Product Queries**: Retrieves product info from knowledge base
- **Inventory Checks**: Real-time inventory via Lambda
- **User Management**: Customer lookup by ID and email
- **Pet Care Advice**: Provides advice from knowledge base
- **Order Processing**: Calculates pricing, discounts, and shipping
- **Business Rules**:
  - 15% discount on orders over $300
  - 10% multi-unit discount
  - Dynamic shipping costs
  - Inventory replenishment alerts

## Observability

The agent includes full OpenTelemetry instrumentation:

- **Service Name**: `langgraph-agent`
- **Dashboard**: CloudWatch GenAI Observability
- **Traces**: Full request/response tracing
- **Metrics**: Performance and usage metrics

## Testing

Invoke the agent runtime:

```python
import boto3
import json
import uuid

client = boto3.client('bedrock-agentcore')
response = client.invoke_agent_runtime(
    agentRuntimeArn='<from-pulumi-output>',
    qualifier='DEFAULT',
    traceId=str(uuid.uuid4()),
    contentType='application/json',
    payload=json.dumps({
        "prompt": "What's the price of Doggy Delights?"
    })
)
```

## Troubleshooting

- **"Knowledge Base not found"**: Ensure KB synced in AWS Console
- **"Docker build failed"**: Check Docker daemon and ECR permissions
- **"Runtime creation failed"**: Verify IAM role permissions and CloudFormation outputs

## Cleanup

```bash
pulumi destroy
```

## Notes

- The agent code is located in the `pet_store_agent` directory
- Docker build uses ARM64 platform for optimal AgentCore performance
- All resources follow AWS best practices
- Configuration is automatically populated from CloudFormation stack outputs
