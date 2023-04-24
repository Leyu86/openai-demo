import asyncio
import json
import uuid

from datastore.datastore import DataStore
from datastore.redis_datastore import get_datastore
from models.models import Document, DocumentMetadata, Organization

DOCUMENT_UPSERT_BATCH_SIZE = 50


async def process_json_dump(filepath: str, datastore: DataStore):
    documents = []
    try:
        with open(filepath) as json_file:
            data = json.load(json_file)

        if data and isinstance(data, list):
            for d in data:
                orgs = d.get("mentioned_organization", [])
                _orgs = []
                for org in orgs:
                    if not org.get("normalized_id"):
                        continue
                    _org = Organization(entity_id=org["normalized_id"], name=org["normalized_name"],
                                        country=org["normalized_country"], logo=org.get("normalized_logo"),
                                        is_startup=org["is_startup"], is_unicorn=org["is_unicorn"])
                    _orgs.append(_org)
                _d = DocumentMetadata(news_id=d["id"], title=d["title"], content=d["content"], url=d["source_url"],
                                      created_at=d["post_time"]["time_ts"], organization=_orgs)
                doc = Document(id=d["id"] or str(uuid.uuid4()), text=d["content"], metadata=_d)
                documents.append(doc)
    except Exception as e:
        print("Error: ", e)

    # do this in batches, the upsert method already batches documents but this allows
    # us to add more descriptive logging
    for i in range(0, len(documents), DOCUMENT_UPSERT_BATCH_SIZE):
        # Get the text of the chunks in the current batch
        batch_documents = documents[i: i + DOCUMENT_UPSERT_BATCH_SIZE]
        print(f"Upserting batch of {len(batch_documents)} documents, batch {i}")
        print("documents: ", documents)
        await datastore.upsert(batch_documents)


async def main():
    # get the arguments
    filepath = "../../data/tesla_news.json"

    # initialize the db instance once as a global variable
    datastore = await get_datastore()
    # process the json dump
    await process_json_dump(filepath, datastore)


if __name__ == "__main__":
    asyncio.run(main())
