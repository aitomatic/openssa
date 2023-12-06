from llama_index import set_global_service_context
from openssa.contrib.custom import CustomSSM
from openssa.utils.llm_config import LLMConfig


def custom_config():
    service_context = LLMConfig.get_service_context_llama_2_70b()
    set_global_service_context(service_context=service_context)
    agent = CustomSSM(
        service_context=service_context,
    )
    print("start reading doc")
    agent.read_directory("tests/doc")
    print("finish reading doc")
    res = agent.discuss("how much does picc weight?")
    print(res)


if __name__ == "__main__":
    custom_config()
