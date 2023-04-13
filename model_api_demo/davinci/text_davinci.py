from component.openai import openai

MODEL = "text-davinci-003"


def completion(prompt: str, model: str = MODEL):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=0,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    print(response)


if __name__ == '__main__':
    input_text = '''Classify the sentiment in these tweets:
    
    1. "I can't stand homework"
    2. "This sucks. I'm bored 😠"
    3. "I can't wait for Halloween!!!"
    4. "My cat is adorable ❤️❤️"
    5. "I hate chocolate"
    
    Tweet sentiment ratings:
    1. Negative
    2. Negative
    3. Positive
    4. Positive
    5. Negative'''
    completion(input_text, model=MODEL)
