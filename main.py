import os
import requests
import json

def generate_fact_set(mentioned_displays):
    facts = []
    for i in range(len(mentioned_displays)):
        facts.append(
            {
                "title": "PIC " + str(i + 1),
                "value": "<at>" + mentioned_displays[i] + "</at>"
            }
        )
    fact_set = {
        "type": "FactSet",
        "facts": facts
    }
    return fact_set

def generate_title(title, color='default'):
    # color: good, dark, attention
    title_block = {
        "type": "TextBlock",
        "size": "Large",
        "wrap": True,
        "weight": "Bolder",
        "color": color,
        "text": title
    }
    return title_block

def generate_description(description):
    description_block = {
        "type": "TextBlock",
        "spacing": "None",
        "text": description,
        "wrap": True
    }
    return description_block

def generate_msteams(mentioned_displays, mentioned_emails):
    entities = []
    for i in range(len(mentioned_displays)):
        entities.append(
            {
                "type": "mention",
                "text": "<at>" + mentioned_displays[i] + "</at>",
                "mentioned": {
                    "id":  mentioned_emails[i],
                    "name": mentioned_displays[i]
                }
            }
        )
    msteams = {
        "entities": entities
    }
    return msteams

def generate_actions(link_displays, link_urls):
    actions = []
    for i in range(len(link_displays)):
        actions.append(
            {
                "type": "Action.OpenUrl",
                "title": link_displays[i],
                "url": link_urls[i]
            }
        )
    return actions

def generate_payload(status, title, description, mentioned_displays, mentioned_emails, link_displays, link_urls):
    color = "default"
    if status == "success":
        color = "good"
    if status == "failed":
        color = "attention"

    json_templates = {
        "type": "message",
        "attachments": [
            {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "type": "AdaptiveCard",
                "body": [
                    generate_title(title, color),
                    generate_description(description),
                    generate_fact_set(mentioned_displays)
                ],
                "actions": generate_actions(link_displays, link_urls),
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.0",
                "msteams": generate_msteams(mentioned_displays, mentioned_emails)
            }
        }]
    }

    return json_templates

def main():
    webhook_url = os.environ["INPUT_WEBHOOK_URL"]
    status = os.environ["INPUT_STATUS"]
    title = os.environ["INPUT_TITLE"]
    description = os.environ["INPUT_DESCRIPTION"]
    tmp_mentioned_display = os.environ["INPUT_MENTIONED_DISPLAY"]
    tmp_mentioned_email = os.environ["INPUT_MENTIONED_EMAIL"]
    tmp_link_display = os.environ["INPUT_LINK_DISPLAY"]
    tmp_link_url = os.environ["INPUT_LINK_URL"]

    mentioned_displays = tmp_mentioned_display.split(',')
    mentioned_emails = tmp_mentioned_email.split(',')
    link_displays = tmp_link_display.split(',')
    link_urls = tmp_link_url.split(',')

    payload = json.dumps(generate_payload(status, title, description, mentioned_displays, mentioned_emails, link_displays, link_urls))
    
    r = requests.post(url = webhook_url, data = payload)
    print(r.text)

if __name__ == "__main__":
    main()
