class OODAPrompts:
    PROVIDE_TOOLS = (
        "You have the following functions available to call, provided here in a dict of function"
        " names and descriptions. {tool_descriptions}"
    )

    FORMULATE_TASK = (
        "Reformulate the user's input as a task (a sentence, not a function call) that could be"
        ' theoretically completed to satisfy the user. Return a JSON dictionary {"content": "your'
        ' thinking here", "task": "your task here"}'
    )

    DECOMPOSE_INTO_SUBTASKS = (
        "Given the tools available, if the task cannot be completed directly with the current tools"
        " and resources, break it down into maximum 2 smaller subtasks that can be directly addressed in"
        " order. If it does not need to be broken down, return an empty list of subtasks."
        ' Return a JSON dictionary {"subtasks": ["subtask 1", "subtask 2", ...]}'
        " each subtask should be a sentence or command or question not a function call."
        " Return json only, nothing else. Think step by step."
    )

    DECOMPOSE_INTO_OODA = (
        "Given the task at hand and the tools available, decompose the task into an OODA procedure."
        ' Return a JSON dictionary {"observe": "instructions for observe step", "orient":'
        ' "instructions for orient step", "decide": "instructions for decide step", "act":'
        ' "instructions for act step"}'
    )

    OBSERVE = (
        "We are in the OBSERVE step. What progress has been made so far? What information do you"
        " have and what can you obtain via the function tools available? Return a JSON dictionary"
        " including the function calls you want to make in the form of function: params."
        ' {"content": "your thinking here", "calls": [{"function1": "params1"}, {"function2":'
        ' "params2"}]}'
    )

    ORIENT = (
        "We are in the ORIENT step. Analyse and reflect on the information obtained. What are the"
        " possible courses of action you can take to complete the task? Return a JSON dictionary"
        ' {"content": "your thinking here"}'
    )

    DECIDE = (
        "We are in the DECIDE step. Choose a course of action to take based on your analysis. What"
        " functions do we need to execute? Return a JSON dictionary including the function calls"
        ' you want to make in the form of function: params. {"content": "your thinking here",'
        ' "calls": [{"function1": "params1"}, {"function2": "params2"}]}'
    )

    ACT = (
        "We are in the ACT step. Given everything so far, finalise your written response to"
        ' complete the task at hand. Return a JSON dictionary {"content": "your response here"}'
    )

    SYNTHESIZE_RESULT = (
        "As an expert in reasoning, you are examining a dialogue involving a user, an assistant, and a system. "
        "Your task is to synthesize the final answer to the user's initial question based on this conversation. "
        "This is the concluding instruction and must be followed with precision. "
        "You will derive the final response by critically analyzing all the messages in the conversation and performing any necessary calculations. "
        "Be aware that some contributions from the assistant may not be relevant or could be misleading due to being based on incomplete information. "
        "{heuristic} "
        "If the conversation does not provide sufficient information to synthesize the answer then admit you cannot produce accurate answer. "
        "Do not use any information outside of the conversation context. "
        "Exercise discernment in selecting the appropriate messages to construct a logical and step-by-step reasoning process."
    )


class BuiltInAgentPrompt:
    COMMUNICATION = (
        "You are an expert in communication. Your will help to format following message with this instruction:\n"
        "###{instruction}###\n\n"
        "Here is the message:\n"
        "###{message}###\n\n"
    )

    PROBLEM_STATEMENT = (
        "You are tasked with constructing the problem statement from a conversation "
        "between a user and an AI chatbot. Your focus should be on the entire context "
        "of the conversation, especially the most recent messages from the user, "
        "to understand the issue comprehensively. Extract specific details "
        "that define the current concerns or questions posed by the user, "
        "which the assistant is expected to address. The problem statement should be "
        "clear, and constructed carefully with complete context and in the user's voice. "
        'Output the response in JSON format with the keyword "problem statement". Think step by step.\n'
        "Example 1:\n"
        "Assistant: Hello, what can I help you with today?\n"
        "User: My boiler is not functioning, please help to troubleshoot.\n"
        "Assistant: Can you check and provide the temperature, pressure, and on-off status?\n"
        "User: The temperature is 120°C.\n\n"
        "Response:\n"
        "{\n"
        '    "problem statement": "Can you help to troubleshoot a non-functioning '
        'boiler, given the temperature is 120°C?"\n'
        "}\n\n"
        "Example 2:\n"
        "Assistant: Hi, what can I help you with?\n"
        "User: I don't know how to go to the airport\n"
        "Assistant: Where are you and which airport do you want to go to?\n"
        "User: I'm in New York\n"
        "Response:\n"
        "{\n"
        '    "problem statement": "How do I get to the airport from my current '
        'location in New York?"\n'
        "}\n\n"
        "Example 3 (Ambiguity):\n"
        "Assistant: How can I assist you today?\n"
        "User: I'm not sure what's wrong, but my computer is acting weird.\n"
        "Assistant: Can you describe the issues you are experiencing?\n"
        "User: Hey I am good, the sky is blue.\n\n"
        "Response:\n"
        "{\n"
        '    "problem statement": ""\n'
        "}\n\n"
        "Example 4 (Multiple Issues):\n"
        "Assistant: What do you need help with?\n"
        "User: My internet is down, and I can't access my email either.\n"
        "Assistant: Are both issues related, or did they start separately?\n"
        "User: They started at the same time, I think.\n\n"
        "Response:\n"
        "{\n"
        '    "problem statement": "Can you help with my internet being down and also '
        'accessing my email?"\n'
        "}"
    )

    ASK_USER = (
        "Your task is to assist an AI assistant in formulating a question for the user. "
        "This should be based on the ongoing conversation, the presented problem statement, "
        "and a specific heuristic guideline. "
        "The assistant should formulate the question strictly based on the heuristic. "
        "If the heuristic does not apply or is irrelevant to the problem statement, "
        "return empty string for the question. "
        "Below is the heuristic guideline:\n"
        "###{heuristic}###\n\n"
        "Here is the problem statement or the user's current question:\n"
        "###{problem_statement}###\n\n"
        'Output the response in JSON format with the keyword "question".'
    )

    ASK_USER_OODA = (
        "Your task is to assist an AI assistant in formulating a question for the user. "
        "This is done through using OODA reasoning. "
        "This should be based on the ongoing conversation, the presented problem statement, "
        "and a specific heuristic guideline. "
        "The assistant should formulate the question strictly based on the heuristic. "
        "If the heuristic does not apply or is irrelevant to the problem statement, "
        "return empty string for the question. "
        "Output the response of ooda reasoning in JSON format with the keyword "
        '"observe", "orient", "decide", "act". Example output key value:\n'
        "\n"
        '    "observe": "Here, articulate your initial assessment of the task, '
        'capturing essential details and contextual elements.",\n'
        '    "orient": "In this phase, analyze and synthesize the gathered '
        'information, considering different angles and strategies.",\n'
        '    "decide": "Now, determine the most suitable action based on your '
        'observations and analysis.",\n'
        '    "act": "The question to ask the user is here."\n '
        "\n\n"
        "Below is the heuristic guideline:\n"
        "###{heuristic}###\n\n"
        "Here is the problem statement or the user's current question:\n"
        "###{problem_statement}###\n\n"
        "Output the JSON only. Think step by step."
    )

    CONTENT_VALIDATION = (
        "You are tasked as an expert in reasoning and contextual analysis. Your "
        "role is to evaluate whether the provided context and past conversation "
        "contain enough information to accurately respond to a given query.\n\n"
        "Please analyze the past conversation and the following context. Then, "
        "determine if the information is sufficient to form an accurate answer. "
        "Respond only in JSON format with the keyword 'is_sufficient'. This "
        "should be a boolean value: True if the information is adequate, and "
        "False if it is not.\n\n"
        "Your response should be in the following format:\n"
        "{{\n"
        '    "is_sufficient": [True/False]\n'
        "}}\n\n"
        "Do not include any additional commentary. Focus solely on evaluating "
        "the sufficiency of the provided context and conversation.\n\n"
        "Context:\n"
        "========\n"
        "{context}\n"
        "========\n\n"
        "Query:\n"
        "{query}\n"
    )

    ANSWER_VALIDATION = (
        "Your role is to act as an expert in reasoning and contextual analysis. "
        "You need to evaluate if the provided answer effectively and clearly addresses the query. "
        "Respond with 'yes' if the answer is clear and confident, and 'no' if it is not. "
        "Here are some examples to guide you: \n\n"
        "Example 1:\n"
        "Query: Can I print a part 50 cm long with this machine?\n"
        "Answer: Given the information and the lack of detailed specifications, "
        "it is not possible to determine if the machine can print a part 50 cm long.\n"
        "Evaluation: no\n\n"
        "Example 2:\n"
        "Query: Can I print a part 50 cm long with this machine?\n"
        "Answer: No, it is not possible to print a part 50 cm long with this machine.\n"
        "Evaluation: yes\n\n"
        "Example 3:\n"
        "Query: How to go to the moon?\n"
        "Answer: I'm sorry, but based on the given context information, "
        "there is no information provided on how to go to the moon.\n"
        "Evaluation: no\n\n"
    )

    SYNTHESIZE_RESULT = (
        "As an expert in problem-solving and contextual analysis, you are to "
        "synthesize an answer for a given query. This task requires you to use "
        "only the information provided in the previous conversation and the "
        "context given below. Your answer should exclusively rely on this "
        "information as the base knowledge.\n\n"
        "Your response must be in JSON format, using the keyword 'answer'. "
        "The format should strictly adhere to the following structure:\n"
        "{{\n"
        '    "answer": "Your synthesized answer here"\n'
        "}}\n\n"
        "Please refrain from including any additional commentary or information "
        "outside of the specified context and past conversation.\n\n"
        "Context:\n"
        "========\n"
        "{context}\n"
        "========\n\n"
        "Query:\n"
        "{query}\n"
    )

    GENERATE_OODA_PLAN = (
        "As a specialist in problem-solving, your task is to utilize the OODA loop "
        "as a cognitive framework for addressing various tasks, which could include "
        "questions, commands, or messages. You have at your disposal a range of tools "
        "to aid in resolving these issues. Your responses should be methodically "
        "structured according to the OODA loop, formatted as a JSON dictionary. "
        "Each dictionary key represents one of the OODA loop's four stages: "
        "Observe, Orient, Decide, and Act. Within each stage, detail your analytical "
        "process and, when relevant, specify the execution of tools, including "
        "their names and parameters. Only output the JSON and nothing else. "
        "The proposed output format is as follows: \n"
        "{\n"
        "    'observe': {\n"
        "        'thought': 'Here, articulate your initial assessment of the task, "
        "capturing essential details and contextual elements.',\n"
        "        'calls': [{'tool_name': '', 'parameters': ''}, ...]  // List tools and "
        "their parameters, if any are used in this stage.\n"
        "    },\n"
        "    'orient': {\n"
        "        'thought': 'In this phase, analyze and synthesize the gathered "
        "information, considering different angles and strategies.',\n"
        "        'calls': [{'tool_name': '', 'parameters': ''}, ...]   // Include any "
        "tools that aid in this analytical phase.\n"
        "    },\n"
        "    'decide': {\n"
        "        'thought': 'Now, determine the most suitable action based on your "
        "observations and analysis.',\n"
        "        'calls': [{'tool_name': '', 'parameters': ''}, ...]   // Specify tools "
        "that assist in making this decision, if applicable.\n"
        "    },\n"
        "    'act': {\n"
        "        'thought': 'Finally, outline the implementation steps based on your "
        "decision, including any practical actions or responses.',\n"
        "        'calls': [{'tool_name': '', 'parameters': ''}, ...]   // List any tools "
        "used in the implementation of the decision.\n"
        "    }\n"
        "}"
    )
