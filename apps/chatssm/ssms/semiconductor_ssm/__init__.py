from ssm.abstract.ssm import SSM, FactSet, InferRuleSet

from dotenv import load_dotenv
from langchain.llms.openai import OpenAIChat


load_dotenv()  # load OpenAI key


ssm = SSM(
    name='Semiconductor SSM',
    description=(
        'I am knowledgeable about semiconductor design & manufacturing '
        'processes'
    ),

    communicator=OpenAIChat(),

    fact_sets=[
        FactSet(storage='facts'),
    ],
    infer_rule_sets=[
        InferRuleSet(storage='infer-rules'),
    ],
)


if __name__ == '__main__':
    print(ssm.process_request(
        'What is your expertise?'))
    print(ssm.process_request(
        'What equipment are you familiar with?'))
    # print(ssm.process_request(
    #     'How would a change in temperature by 3 degrees '
    #     'impact the deposition rate?'))
    print(ssm.process_request(
        'What are the potential bottlenecks in the ALD process?'))
    print(ssm.process_request(
        'What improvements can be made in the ALD process to increase yield?'))
    print(ssm.process_request(
        'Can you suggest an efficient sequence of steps for the ALD process '
        'with Silicon Dioxide (SiO2)?'))
    print(ssm.process_request(
        'Estimate Total Time for 5 cycles, each with '
        'Pulse Time = 5 and Purge Time = 3.'))
    print(ssm.process_request(
        'Estimate Deposition Rate given Thickness = 400 Angstroms'
        'after Total Time = 60 seconds.'
        'Answer me in JSON.'))
