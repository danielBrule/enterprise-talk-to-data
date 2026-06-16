from openai import AsyncAzureOpenAI
from typing import List, Dict, Any

from backend.app.core.config import settings


class LLMService:
    def __init__(self):
        if not all(
            [
                settings.azure_openai_endpoint,
                settings.azure_openai_api_key,
                settings.azure_openai_api_version,
            ]
        ):
            raise ValueError(
                "Azure OpenAI configuration is incomplete. Please set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, and AZURE_OPENAI_API_VERSION."
            )

        deployment_for_client = (
            settings.azure_openai_default_deployment
            or settings.azure_openai_schema_retrieval_deployment
            or settings.azure_openai_sql_generation_deployment
            or settings.azure_openai_summary_deployment
        )

        if not deployment_for_client:
            raise ValueError(
                "Azure OpenAI model deployment is not configured. Set AZURE_OPENAI_DEPLOYMENT or one of the task-specific deployment environment variables."
            )

        self.client = AsyncAzureOpenAI(
            azure_endpoint=settings.azure_openai_endpoint,
            api_key=settings.azure_openai_api_key,
            api_version=settings.azure_openai_api_version,
        )

    async def generate_response(
        self,
        messages: List[Dict[str, Any]],
        *,
        task: str | None = None,
        model: str | None = None,
        **kwargs,
    ) -> str:
        """
        Generate a response from the Azure OpenAI model.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            task: Optional task name used to select a task-specific model deployment.
            model: Optional explicit deployment/model name to use instead of task lookup.
            **kwargs: Additional parameters for the completion (e.g., temperature, max_tokens)

        Returns:
            The generated response content
        """
        if model is None:
            model = settings.get_azure_openai_deployment(task)
        print(f"Using model deployment: {model} for task: {task}")
        print("Azure endpoint:", settings.azure_openai_endpoint)
        if not model:
            raise ValueError(
                "Azure OpenAI model deployment is not configured. Set AZURE_OPENAI_DEPLOYMENT or the task-specific deployment environment variable."
            )

        response = await self.client.chat.completions.create(
            model=model, messages=messages, **kwargs
        )
        return response.choices[0].message.content

    async def generate_schema_retrieval(
        self,
        messages: List[Dict[str, Any]],
        **kwargs,
    ) -> str:
        return await self.generate_response(messages, task="schema_retrieval", **kwargs)

    async def generate_sql_generation(
        self,
        messages: List[Dict[str, Any]],
        **kwargs,
    ) -> str:
        return await self.generate_response(messages, task="sql_generation", **kwargs)

    async def generate_summary(
        self,
        messages: List[Dict[str, Any]],
        **kwargs,
    ) -> str:
        return await self.generate_response(messages, task="summary", **kwargs)
