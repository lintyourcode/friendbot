import os

import dotenv
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

from friendbot.agent import Agent
from friendbot.discord import DiscordClient
from friendbot.trigger import Trigger


def main():
    dotenv.load_dotenv()

    if not os.getenv("FRIENDBOT_NAME"):
        raise ValueError("FRIENDBOT_NAME environment variable must be set")
    name = os.getenv("FRIENDBOT_NAME")

    if not os.getenv("FRIENDBOT_IDENTITY"):
        raise ValueError("FRIENDBOT_IDENTITY environment variable must be set")
    identity = os.getenv("FRIENDBOT_IDENTITY")

    if not os.getenv("DISCORD_TOKEN"):
        raise ValueError("DISCORD_TOKEN environment variable must be set")
    discord_token = os.getenv("DISCORD_TOKEN")

    if not os.getenv("PINECONE_API_KEY"):
        raise ValueError("PINECONE_API_KEY environment variable must be set")
    if not os.getenv("PINECONE_INDEX_NAME"):
        raise ValueError("PINECONE_INDEX_NAME environment variable must be set")
    index_name = os.getenv("PINECONE_INDEX_NAME")

    pinecone = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    if index_name not in [index.name for index in pinecone.list_indexes()]:
        pinecone.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud=os.getenv("PINECONE_CLOUD", "aws"),
                region=os.getenv("PINECONE_REGION", "us-west-2"),
            ),
        )
    # TODO: Rename `friend` to `agent`
    friend = Agent(
        name=name,
        identity=identity,
        moderate_messages=os.getenv("FRIENDBOT_MODERATE_MESSAGES"),
        pinecone_index=pinecone.Index(index_name),
        embedding_model=os.getenv(
            "FRIENDBOT_EMBEDDING_MODEL", "text-embedding-3-small"
        ),
    )
    # TODO: Rename `proctor` to `discord`
    proctor = DiscordClient(friend=friend)
    Trigger(proctor, friend)
    proctor.run(discord_token)
