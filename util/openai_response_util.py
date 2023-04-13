from util.tiktoken_util import num_tokens_from_messages


def format_response(request: dict, response: dict):
    """Format the response from OpenAI's API."""
    if request is None or response is None:
        return None
    print('--------------------------------------------------------------------------------')

    print('\n### Prompt ###')
    for message in request.get('messages', []):
        print(f'[{message["role"] if message.get("name") is None else message["name"]}]: {message["content"]}')

    try:
        print('\n### Completion ###')
        choices = response['choices']
        for choice in choices:
            message = choice['message']
            if message:
                print(f"{message['role']}: {message['content']}")

        print('\n### Prompt Tokens ###')
        # print(f"{num_tokens_from_messages(request.get('messages', []), request.get('model', 'gpt-3.5-turbo'))} prompt tokens counted by num_tokens_from_messages().")
        print(f'{response["usage"]["prompt_tokens"]} prompt tokens counted by the OpenAI API.')

        print('--------------------------------------------------------------------------------')
    except Exception as e:
        print(response)
        print(e)

    return response
