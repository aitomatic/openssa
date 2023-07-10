from dotenv import load_dotenv
from langchain.llms.openai import OpenAIChat
from ssm.abstract.ssm import SSM, FactSet, InferRuleSet


load_dotenv()  # load OpenAI key


ssm = SSM(
    name='Industrial Boiler SSM',
    description=(
        'I am knowledgeable about the design, operation and troubleshooting '
        'of industrial boilers / steamers.'
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
    print(ssm.process_request('What is your expertise?'))
    print(ssm.process_request('What boiler types are you familar with?'))
    # print(ssm.process_request('State your inference rule(s)?'))
