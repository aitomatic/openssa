import os
from dotenv import load_dotenv
from langchain.llms.openai import OpenAIChat
from openssm.abstract.ssm import SSM, FactSet, InferRuleSet


load_dotenv()

dir_path = os.path.dirname(__file__)


semi_ald_ssm = SSM(
    name='Semiconductor SSM',
    description=(
        'I am knowledgeable about semiconductor design & manufacturing '
        'processes, particularly Atomic Layer Deposition (ALD).'
    ),

    slm=OpenAIChat(),

    fact_sets=[
        FactSet(storage=f'{dir_path}/facts'),
    ],
    infer_rule_sets=[
        InferRuleSet(storage=f'{dir_path}/infer-rules'),
    ],
)


if __name__ == '__main__':
    print(semi_ald_ssm.process_request(
        'What is your expertise?'))
    print(semi_ald_ssm.process_request(
        'What equipment are you familiar with?'))
    print(semi_ald_ssm.process_request(
        'What are the potential bottlenecks in the ALD process? '
        'Answer me in a ranked bullet-point list.'))
    print(semi_ald_ssm.process_request(
        'What improvements can be made in the ALD process to increase yield?'))
    print(semi_ald_ssm.process_request(
        'Can you suggest an efficient sequence of steps for the ALD process '
        'with Silicon Dioxide (SiO2)? '
        'Answer me in bullet-point list.'))
    print(semi_ald_ssm.process_request(
        'Estimate Total Time for 5 cycles, each with '
        'Pulse Time = 5 and Purge Time = 3.'))
    print(semi_ald_ssm.process_request(
        'Estimate Deposition Rate (stating unit) '
        'given Thickness = 400 Angstroms after Total Time = 60 seconds. '
        'Answer me in JSON.'))
