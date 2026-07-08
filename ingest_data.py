import json
import os
import sys
import logging
from typing import List, Dict, Any

from algoliasearch.search.client import SearchClientSync

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def load_payload(filepath: str) -> List[Dict[str, Any]]:
    if not os.path.exists(filepath):
        logger.error(f"Data ingestion failed: Payload file not found at path: {filepath}")
        sys.exit(1)        
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            logger.info(f"Successfully loaded {len(data)} objects from {filepath}")
            return data
    except json.JSONDecodeError as e:
        logger.error(f"Data ingestion failed: Error decoding JSON from {filepath}: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred while reading the payload: {e}")
        sys.exit(1)

def push_to_algolia(records: List[Dict[str, Any]], index_name: str) -> None:
    app_id = os.getenv("ALGOLIA_APP_ID")
    api_key = os.getenv("ALGOLIA_API_KEY")
    
    if not app_id or not api_key:
        logger.error("Missing Credentials: Environment variables ALGOLIA_APP_ID and ALGOLIA_API_KEY must be set.")
        sys.exit(1)
        
    try:
        logger.info("Establishing connection to Algolia...")
        client = SearchClientSync(app_id, api_key)
        
        logger.info(f"Pushing records to Algolia index '{index_name}'...")
        
        # Call save_objects directly on the client and utilize wait_for_tasks for synchronization
        client.save_objects(
            index_name=index_name,
            objects=records,
            wait_for_tasks=True
        )
            
        logger.info("Success: All records have been successfully pushed and indexed in Algolia.")
        
    except Exception as e:
        logger.error(f"API Error: An error occurred while communicating with Algolia: {e}")
        sys.exit(1)

if __name__ == "__main__":
    PAYLOAD_FILE = "expected_payload.json"
    INDEX_NAME = "alpha" 
    
    logger.info("Initializing Algolia data ingestion script...")

    unified_payload = load_payload(PAYLOAD_FILE)
    
    push_to_algolia(unified_payload, INDEX_NAME)
    
    logger.info("Data ingestion process completed successfully.")