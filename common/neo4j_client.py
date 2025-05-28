import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load .env file
load_dotenv()

# Neo4j connection config
NEO4J_URI = os.environ.get("NEO4J_URI")
NEO4J_USER = os.environ.get("NEO4J_USERNAME")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD")
NEO4J_INSTANCE_NAME = os.environ.get("AURA_INSTANCENAME")
NEO4J_INSTANCE_ID = os.environ.get("AURA_INSTANCEID")

# Singleton driver instance
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def get_neo4j_driver():
    """Return Neo4j driver instance."""
    return driver


def close_driver():
    """Close Neo4j driver connection."""
    driver.close()
