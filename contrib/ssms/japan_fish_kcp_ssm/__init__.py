from dotenv import load_dotenv
from langchain.llms.openai import OpenAIChat
from ssm.abstract.ssm import SSM, FactSet, InferRuleSet

load_dotenv()  # load OpenAI key


ssm = SSM(
    name='Expert Japanese Fisherman SSM',
    description=(
        'I am knowledgeable about commonness of and ideal fishing conditions '
        'for various types of commercially-valuable fish in the Sea of Japan'
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
    print(ssm.process_request('What fish types do you know about?'))
    print(ssm.process_request('State your inference rule(s)?'))
