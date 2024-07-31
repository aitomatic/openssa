from openssa.l2.util.lm.huggingface_lm import HuggingFaceLM
from openssa.l2.util.lm.config import LMConfig

lm = HuggingFaceLM(model=LMConfig.DEFAULT_HF_LLAMA_MODEL, api_base=LMConfig.LLAMA_API_URL)
