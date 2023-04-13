import backoff

import config
from component.openai import openai
from util.openai_response_util import format_response
from util.retry_with_exponential_backoff import retry_with_exponential_backoff


def chat_completion(model, messages: list, prompt='', max_tokens=1000, temperature=0, top_p=1):
    openai.api_key = config.OPENAI_API_KEY
    if model in ["gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-4", "gpt-4-0314"]:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )
    else:
        response = openai.Completion.create(
            model=model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )
    format_response({'model': model, 'messages': messages}, response)


@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def completions(**kwargs):
    openai.api_key = config.OPENAI_API_KEY
    return openai.Completion.create(**kwargs)


@retry_with_exponential_backoff
def chat_completions_with_exponential_backoff(**kwargs):
    openai.api_key = config.OPENAI_API_KEY
    return openai.ChatCompletion.create(**kwargs)
