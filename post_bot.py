import os
import requests
import json
import logging
import time
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

DISCOURSE_URL = os.getenv("DISCOURSE_URL")
API_KEY = os.getenv("API_KEY")
API_USERNAME = os.getenv("API_USERNAME")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("discourse_topics.log"), logging.StreamHandler()]
)

HEADERS = {
    "Api-Key": API_KEY,
    "Api-Username": API_USERNAME,
    "Content-Type": "application/json"
}

RETRY_LIMIT = 3
RATE_LIMIT_DELAY = 1

def create_topic(title, body, category=None, image_url=None, image_position="end", formatting=None, embed_url=None, external_id=None):
    url = f"{DISCOURSE_URL}/posts.json"
    data = {
        "title": title,
        "raw": body,
        "category": category,
        "embed_url": embed_url,
        "external_id": external_id
    }

    data = {k: v for k, v in data.items() if v is not None}

    if formatting:
        if formatting.get("bold"):
            body = f"**{body}**"
        if formatting.get("italic"):
            body = f"*{body}*"
        if formatting.get("header"):
            body = f"# {body}"

    if image_url:
        image_markdown = f"![Image]({image_url})"
        if image_position == "start":
            body = f"{image_markdown}\n\n{body}"
        elif image_position == "end":
            body = f"{body}\n\n{image_markdown}"
        elif image_position == "inline":
            body = body.replace("[IMAGE]", image_markdown)

    data["raw"] = body

    for attempt in range(RETRY_LIMIT):
        try:
            response = requests.post(url, headers=HEADERS, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            logging.error(f"Attempt {attempt + 1} failed: {err}")
            time.sleep(2)
    return None

def load_topics_from_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            topics = json.load(file)
            if isinstance(topics, dict):
                return [topics]
            return topics
    except Exception as e:
        logging.error(f"Failed to load topics from file: {e}")
        return []

if __name__ == "__main__":
    topics_file = "topics.json"
    topics = load_topics_from_json(topics_file)

    if topics:
        for topic in tqdm(topics, desc="Creating Topics", unit="topic"):
            title = topic.get("title")
            body = topic.get("body", "")
            category = topic.get("category")
            image_url = topic.get("image_url")
            image_position = topic.get("image_position", "end")
            formatting = topic.get("formatting", {})
            embed_url = topic.get("embed_url")
            external_id = topic.get("external_id")

            response = create_topic(title, body, category, image_url, image_position, formatting, embed_url, external_id)

            if response:
                logging.info(f"Created topic '{title}' with ID {response['post_number']}")
            else:
                logging.error(f"Failed to create topic '{title}'")
    else:
        logging.error("No topics to process. Please check the JSON file.")
