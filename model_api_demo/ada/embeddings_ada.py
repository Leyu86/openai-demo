from openai.embeddings_utils import get_embedding
from util.tiktoken_util import chunked_tokens
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_not_exception_type
import numpy as np

from component.openai import openai

EMBEDDING_MODEL = 'text-embedding-ada-002'
EMBEDDING_CTX_LENGTH = 8191
EMBEDDING_ENCODING = 'cl100k_base'


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6),
       retry=retry_if_not_exception_type(openai.InvalidRequestError))
def get_embedding(text, model=EMBEDDING_MODEL):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']


def len_safe_get_embedding(text, model=EMBEDDING_MODEL, max_tokens=EMBEDDING_CTX_LENGTH,
                           encoding_name=EMBEDDING_ENCODING, average=True):
    chunk_embeddings = []
    chunk_lens = []
    for chunk in chunked_tokens(text, encoding_name=encoding_name, chunk_length=max_tokens):
        chunk_embeddings.append(get_embedding(chunk, model=model))
        chunk_lens.append(len(chunk))

    if average:
        chunk_embeddings = np.average(chunk_embeddings, axis=0, weights=chunk_lens)
        chunk_embeddings = chunk_embeddings / np.linalg.norm(chunk_embeddings)  # normalizes length to 1
        chunk_embeddings = chunk_embeddings.tolist()
    return chunk_embeddings


if __name__ == '__main__':
    print(get_embedding("Hello world!"))
