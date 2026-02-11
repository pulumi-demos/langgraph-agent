FROM --platform=linux/arm64 public.ecr.aws/docker/library/python:3.12-slim-bookworm

WORKDIR /app

COPY pet_store_agent/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install bedrock-agentcore aws-opentelemetry-distro

COPY pet_store_agent/*.py ./

ENV AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}
ENV KNOWLEDGE_BASE_1_ID=${KNOWLEDGE_BASE_1_ID}
ENV KNOWLEDGE_BASE_2_ID=${KNOWLEDGE_BASE_2_ID}
ENV SYSTEM_FUNCTION_1_NAME=${SYSTEM_FUNCTION_1_NAME}
ENV SYSTEM_FUNCTION_2_NAME=${SYSTEM_FUNCTION_2_NAME}

ENV OTEL_PYTHON_DISTRO=aws_distro
ENV OTEL_PYTHON_CONFIGURATOR=aws_configurator
ENV OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
ENV OTEL_TRACES_EXPORTER=otlp
ENV OTEL_EXPORTER_OTLP_LOGS_HEADERS=x-aws-log-group=agents/langgraph-agent-logs,x-aws-log-stream=default,x-aws-metric-namespace=agents
ENV OTEL_RESOURCE_ATTRIBUTES=service.name=langgraph-agent
ENV AGENT_OBSERVABILITY_ENABLED=true

EXPOSE 8080

CMD ["opentelemetry-instrument", "python", "agentcore_entrypoint.py"]
