from model_api_demo import completion

MODEL = "gpt-3.5-turbo"

messages = [
    {"role": "system", "content": "You are a helpful, pattern-following assistant."},
    {"role": "system", 'name': 'example_user',
     "content": "Help me translate the following corporate jargon into plain English."},
    {"role": "system", 'name': 'example_assistant', "content": "Sure, I'd be happy to!"},
    {"role": "system", 'name': 'example_user', "content": "New synergies will help drive top-line growth."},
    {"role": "system", 'name': 'example_assistant',
     "content": "Things working well together will increase revenue."},
    {"role": "system", 'name': 'example_user',
     "content": "Let's circle back when we have more bandwidth to touch base on opportunities for increased leverage."},
    {"role": "system", 'name': 'example_assistant',
     "content": "Let's talk later when we're less busy about how to do better."},
    {"role": "user",
     "content": "This late pivot means we don't have time to boil the ocean for the client deliverable."},
]


def chat_completion():
    completion.chat_completion(model=MODEL, messages=messages)


def completions_with_exponential_backoff():
    return completion.chat_completions_with_exponential_backoff(model=MODEL, messages=messages)


if __name__ == '__main__':
    res = completions_with_exponential_backoff()
    print(res)
