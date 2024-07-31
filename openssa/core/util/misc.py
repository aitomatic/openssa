type AskAnsPair = tuple[str, str]


def format_other_result(other_result: AskAnsPair) -> str:
    question, answer = other_result
    return (f'======================\n'
            'ADDITIONAL INFORMATION:\n'
            '\n'
            'QUESTION:\n'
            '-----------------------\n'
            f'{question}\n'
            '-----------------------\n'
            '\n'
            'ANSWER:\n'
            '-----------------------\n'
            f'{answer}\n'
            '-----------------------\n'
            '=======================\n')
