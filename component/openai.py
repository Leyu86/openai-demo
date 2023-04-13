import config
import openai


def openai_client():
    openai.api_key = config.OPENAI_API_KEY
    return openai


openai = openai_client()
