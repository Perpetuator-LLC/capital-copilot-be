"""
Copyright (c) 2024 Perpetuator LLC

This file is part of Capital Copilot by Perpetuator LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

import logging
import os
import sys

from git import Repo
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from copilot.copilot_shared import process_env


def main():
    process_env()
    logging.getLogger().setLevel(os.getenv("LOG_LEVEL", "INFO"))
    script_dir = os.path.dirname(os.path.realpath(__file__))
    repo_dir = os.path.realpath(os.path.join(script_dir, ".."))

    old_tag = "v0.4.0"
    new_tag = "v0.5.0"

    repo = Repo(repo_dir)
    assert not repo.bare

    if not tag_exists(repo, old_tag):
        logging.error(f"Old tag '{old_tag}' does not exist in the repository.")
        sys.exit(1)

    if tag_exists(repo, new_tag):
        changelog = get_changes_between_tags(repo_dir, old_tag, new_tag)
        logging.info(f"Generating changelog between tags {old_tag} and {new_tag}")
    else:
        changelog = generate_changelog_since_tag(repo_dir, old_tag)
        logging.info(f"Tag '{new_tag}' does not exist, generating changelog from {old_tag} to current HEAD")

    logging.info("--- Changelog extracted from git commits")
    logging.info(changelog)
    logging.info("--- Changelog summary")
    summary = summarize(changelog, old_tag, new_tag)

    file_path = os.path.join(repo_dir, "CHANGELOG.md")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            original_content = file.read()
        with open(file_path, "w") as file:
            file.write(summary + "\n\n\n" + original_content)
    else:
        with open(file_path, "w+") as file:
            file.write(summary)

    logging.info("Changelog generated successfully")


def tag_exists(repo, tag_name):
    """Check if a tag exists in the repository."""
    return any(tag.tag for tag in repo.tags if tag.name == tag_name)


def generate_changelog_since_tag(repo_path, tag):
    repo = Repo(repo_path)
    assert not repo.bare
    commits = list(repo.iter_commits(f"{tag}..HEAD"))
    changelog = f"Changelog since {tag}\n\n"
    for commit in commits:
        changelog += f"- {commit.summary}\n"
    return changelog


def get_changes_between_tags(repo_path, old_tag, new_tag):
    repo = Repo(repo_path)
    assert not repo.bare
    commits = list(repo.iter_commits(f"{old_tag}...{new_tag}"))
    changelog = f"Changelog from {old_tag} to {new_tag}\n\n"
    for commit in commits:
        changelog += f"- {commit.summary}\n"
    return changelog


def summarize(changelog, old_tag, new_tag):
    chat = ChatOpenAI(temperature=0)
    chat.model_name = "gpt-4"
    messages = [
        SystemMessage(
            content="Your directive is to summarize git commits into a changelog that will go into a markdown file. "
            "There should be a paragraph that summarizes the changes. "
            "This changelog is for a financial research web application. Squeeze is an indicator used in "
            "technical analysis of stock prices. "
            "The response should conform (and additional sections can be added if deemed necessary) to: "
            f"# Changelog from {old_tag} to {new_tag} part.\n\n"
            "<summary>\n\n"
            "## Enhancements\n"
            "<list_of_enhancements>\n\n"
            "## Cleanups"
            "<list_of_cleanups>"
        ),
        HumanMessage(content=f"Convert the following commits into a summary: {changelog}"),
    ]
    response = chat.invoke(messages)
    logging.info(response.content)
    return response.content


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"main caught exception: {e}", exc_info=e)
        sys.exit(1)
