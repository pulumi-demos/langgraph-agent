# LangGraph ReAct Agent on AWS Bedrock AgentCore

Deploy a production-ready LangGraph ReAct agent to AWS Bedrock AgentCore using Pulumi.

## Quick Start

```bash
# 1. Deploy CloudFormation stack (Knowledge Bases, Lambdas)
aws cloudformation create-stack \
  --stack-name pet-store-kb \
  --template-body file://pet_store_knowledge_bases.yaml \
  --capabilities CAPABILITY_IAM

# 2. Sync Knowledge Bases in AWS Console (Bedrock → Knowledge Bases)

# 3. Install dependencies with UV
uv sync

# 4. Configure Pulumi with CloudFormation outputs
uv run python setup_config.py pet-store-kb

# 5. Deploy infrastructure
pulumi up
```

## What Gets Deployed

- **ECR Repository**: Stores agent Docker image (ARM64)
- **Docker Image**: LangGraph agent with OpenTelemetry
- **AgentCore Runtime**: Serverless runtime integrated with Knowledge Bases, Lambda, and Guardrails

## Prerequisites

- AWS CLI configured
- Python 3.12+
- [UV](https://docs.astral.sh/uv/) package manager
- Pulumi CLI
- Docker (for building agent image)
- CloudFormation stack with Knowledge Bases (synced)
- Lambda functions deployed
- Guardrails configured

## Configuration

Edit `Pulumi.dev.yaml` or run `uv run python setup_config.py <stack-name>`:

```yaml
config:
  knowledgeBaseStackOutputs:
    ProductInfo1stKnowledgeBaseId: "kb-id-1"
    PetCare2ndKnowledgeBaseId: "kb-id-2"
    SolutionAccessRoleArn: "arn:aws:iam::account:role/Role"
    PetStoreInventoryManagement1stFunction: "function-name"
    PetStoreUserManagement2ndFunction: "function-name"
    PetStoreGuardrailId: "guardrail-id"
    PetStoreGuardrailVersion: "1"
```

## Agent Features

**Tools**: Product info retrieval, pet care advice, inventory check, user lookup (by ID/email)

**Business Logic**: Multi-unit discounts (10%), order discounts (15% >$300), dynamic shipping, inventory alerts

**Observability**: OpenTelemetry traces in CloudWatch GenAI dashboard

## Testing

```python
import boto3, json, uuid

client = boto3.client('bedrock-agentcore')
response = client.invoke_agent_runtime(
    agentRuntimeArn='<from-pulumi-output>',
    qualifier='DEFAULT',
    traceId=str(uuid.uuid4()),
    contentType='application/json',
    payload=json.dumps({"prompt": "What's the price of Doggy Delights?"})
)
```

## Outputs

```bash
pulumi stack output agent_runtime_arn    # For invocation
pulumi stack output agent_runtime_name   # For evaluation
```

## Troubleshooting

- **"Knowledge Base not found"**: Ensure KB synced in AWS Console
- **"Docker build failed"**: Check Docker daemon and ECR permissions
- **"Runtime creation failed"**: Verify IAM role permissions

## Monitoring

CloudWatch → GenAI Observability → Service: `langgraph-agent`

## Cleanup

```bash
pulumi destroy
```

## Resources

- [Pulumi Docker Build](https://www.pulumi.com/registry/packages/docker-build/)
- [AWS Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/)
- [LangGraph](https://langchain-ai.github.io/langgraph/)
