from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion


def init_kernel():
    kernel = Kernel()
    kernel.add_service(OpenAIChatCompletion(
        service_id="chat-gpt",
        ai_model_id="gpt-3.5-turbo",
        api_key='your_openai_api_key',  # Ideally fetched from environment variables
    ))
    return kernel
