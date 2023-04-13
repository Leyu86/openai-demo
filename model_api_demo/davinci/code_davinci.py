from component.openai import openai

MODEL = "code-davinci-003"


def code_completion(prompt: str, model: str = "MODEL"):
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
