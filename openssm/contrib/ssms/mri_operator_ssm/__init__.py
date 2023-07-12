import os

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

from ssm.abstract.ssm import SSM, FactSet, InferRuleSet

load_dotenv()

dir_path = os.path.dirname(__file__)


ssm = SSM(
    name='MRI Operator SSM',
    description=(
        'I am knowledgeable about MRI operations, physics, imaging, and parameter tuning protocols.'
    ),

    slm=ChatOpenAI(),

    fact_sets=[
        FactSet(storage=f'{dir_path}/facts'),
    ],
    infer_rule_sets=[
        InferRuleSet(storage=f'{dir_path}/infer-rules'),
    ]
)


if __name__ == '__main__':
    print(ssm.process_request(
        'What is your expertise?'))
    print(ssm.process_request(
        'What equipment are you familiar with?'))
    print(ssm.process_request(
        'What is the difference between a 1.5T and 3T MRI?'))
    print(ssm.process_request(
        'How do I tune the parameters for a 3T MRI?'))
    print(ssm.process_request(
        'What parameters do I tune if we are investigating a brain tumor?'))

