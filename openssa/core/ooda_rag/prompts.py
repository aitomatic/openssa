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

    # " For example, if the user input is 'Was Obama"
    # " born on an odd or even day?', the task could be 'Determine whether Obama was born on an"
    # " odd or even day.' If the input is 'I need to get to the airport.', the task could be 'Get"
    # " to the airport.' If the input is 'I am getting error code 404.', the task could be 'Fix"
    # " error code 404."

    DECOMPOSE_INTO_SUBTASKS = (
        "Given the tools available, if the task cannot be completed directly with the current tools"
        " and resources, break it down into smaller subtasks that can be directly addressed in"
        " order. If it does not need to be broken down, return an empty list of subtasks."
        ' Return a JSON dictionary {"subtasks": ["subtask 1", "subtask 2", ...]}'
        " each subtask should be a sentence or question not a function call."
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

    # SYNTHESIZE_RESULT = (
    #     "You are an reasoning expert. You are reviewing a conversation between user, assistant and system. "
    #     "This is the final message and instruction, so follow this extremely carefully. "
    #     "You will produce the final result for user question (the first message in the conversation) "
    #     "by reasoning through all messages and doing calculations if needed. "
    #     "The challenging is some of messages from assistants might not be useful, or even misleading since it is synthesized from unsufficient information. "
    #     "So you need to consider available information carefully to pick the right messages to reasonign step by step. "
    # )

    SYNTHESIZE_RESULT = (
        "As an expert in reasoning, you are examining a dialogue involving a user, an assistant, and a system. "
        "Your task is to synthesize the final answer to the user's initial question based on this conversation. "
        "This is the concluding instruction and must be followed with precision. "
        "You will derive the final response by critically analyzing all the messages in the conversation and performing any necessary calculations. "
        "Be aware that some contributions from the assistant may not be relevant or could be misleading due to being based on incomplete information. "
        "Exercise discernment in selecting the appropriate messages to construct a logical and step-by-step reasoning process."
    )
