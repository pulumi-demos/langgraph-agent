"""LangGraph ReAct Agent on AWS Bedrock AgentCore Infrastructure"""
import pulumi
import pulumi_aws as aws
import pulumi_aws_native as aws_native
import pulumi_docker_build as docker_build

# Get current AWS region
region = aws.get_region()

# Configuration
config = pulumi.Config()
kb_stack_outputs = config.require_object("knowledgeBaseStackOutputs")

product_info_kb_id = kb_stack_outputs["ProductInfo1stKnowledgeBaseId"]
pet_care_kb_id = kb_stack_outputs["PetCare2ndKnowledgeBaseId"]
solution_role_arn = kb_stack_outputs["SolutionAccessRoleArn"]
inventory_function_name = kb_stack_outputs["PetStoreInventoryManagement1stFunction"]
user_function_name = kb_stack_outputs["PetStoreUserManagement2ndFunction"]

# ECR Repository
ecr_repo = aws.ecr.Repository(
    "langgraph-agent-repo",
    name="langgraph-agent-repo",
    image_scanning_configuration={"scanOnPush": True},
    force_delete=True
)

# Get ECR credentials
ecr_creds = aws.ecr.get_authorization_token_output(registry_id=ecr_repo.registry_id)

# Build and push Docker image
image = docker_build.Image(
    "langgraph-agent-image",
    dockerfile=docker_build.DockerfileArgs(location="Dockerfile"),
    context=docker_build.BuildContextArgs(location="."),
    platforms=[docker_build.Platform.LINUX_ARM64],
    push=True,
    registries=[docker_build.RegistryArgs(
        address=ecr_repo.repository_url,
        username=ecr_creds.user_name,
        password=ecr_creds.password
    )],
    tags=[ecr_repo.repository_url.apply(lambda url: f"{url}:latest")],
    opts=pulumi.ResourceOptions(depends_on=[ecr_repo])
)

# Create AgentCore Runtime using aws-native provider
agent_runtime = aws_native.bedrockagentcore.Runtime(
    "langgraph-agentcore-runtime",
    agent_runtime_name="LangGraphAgentCoreRuntime",
    role_arn=solution_role_arn,
    agent_runtime_artifact=aws_native.bedrockagentcore.RuntimeAgentRuntimeArtifactArgs(
        container_configuration=aws_native.bedrockagentcore.RuntimeContainerConfigurationArgs(
            container_uri=image.ref
        )
    ),
    network_configuration=aws_native.bedrockagentcore.RuntimeNetworkConfigurationArgs(
        network_mode=aws_native.bedrockagentcore.RuntimeNetworkMode.PUBLIC
    ),
    environment_variables={
        'AWS_DEFAULT_REGION': region.name,
        'KNOWLEDGE_BASE_1_ID': product_info_kb_id,
        'KNOWLEDGE_BASE_2_ID': pet_care_kb_id,
        'SYSTEM_FUNCTION_1_NAME': inventory_function_name,
        'SYSTEM_FUNCTION_2_NAME': user_function_name
    },
    lifecycle_configuration=aws_native.bedrockagentcore.RuntimeLifecycleConfigurationArgs(
        max_lifetime=60
    ),
    opts=pulumi.ResourceOptions(depends_on=[image])
)

# Exports
pulumi.export("ecr_repository_url", ecr_repo.repository_url)
pulumi.export("image_uri", image.ref)
pulumi.export("agent_runtime_id", agent_runtime.agent_runtime_id)
pulumi.export("agent_runtime_arn", agent_runtime.agent_runtime_arn)
pulumi.export("agent_runtime_name", agent_runtime.agent_runtime_name)
pulumi.export("agent_runtime_status", agent_runtime.status)
