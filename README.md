# Discourse Topic Creation Script

This Python script allows you to create topics on a Discourse forum using the Discourse API. It can handle both single and multiple topics, with support for custom formatting, image embedding, and category assignment.

## Requirements

- Python 3.x
- `requests` library
- `python-dotenv` library
- `tqdm` library (for progress tracking)

## Setup

1. Clone the repository or download the script.
2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory with the following content:

    ```env
    DISCOURSE_URL=https://your-discourse-site.com
    API_KEY=your-api-key-here
    API_USERNAME=your-username-here
    ```

## Usage

1. Prepare a `topic.json` (single topic) or `topics.json` (multiple topics) file.
2. Run the script:

    ```bash
    python create_discourse_topics.py
    ```

The script will load topics from the provided JSON file, create them on your Discourse site, and log the results.

## Features

- Supports creating a single topic or multiple topics.
- Handles markdown formatting, image embedding, and external URLs.
- Configurable retry limit and rate-limiting delay for API calls.

## Logging

Logs are saved to `discourse_topics.log` and will also be printed to the console.

---
