import os

from loguru import logger

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from prepare.prepare_paper_data import call_paper_data_api


# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.message("test")
def message_hello(message, say):
    response = call_paper_data_api()
    # logger.info(response)
    
    sections = []
    for r in response["datas"][:3]:
        r['title'] = r['title'].replace('\n', '')
        r['summary'] = r['summary'][:300].replace('\n', '')
        sections.extend([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*<{r['id']}|{r['title']}>*"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "emoji": True,
                        "text": f"著者: {r['author']}\n{r['summary']}..."
                    }
                ]
            },
            {"type": "divider"}
        ])
    
    
    
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "今週のおすすめAI関連論文を紹介します！"
                }
            },
            {"type": "divider"}
        ] + sections + [
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "もっと見る",
                            "emoji": True
                        },
                        "value": "show-more",
                        "action_id": "show-more"
                    }
                ]
            }
        ]
    )

@app.action("show-more")
def action_button_click_show_more(ack, body, client):
    # アクションを確認したことを即時で応答します
    ack()
    
    response = call_paper_data_api()
    sections = []
    for r in response["datas"]:
        r['title'] = r['title'].replace('\n', '')
        r['summary'] = r['summary'][:300].replace('\n', '')
        sections.extend([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*<{r['id']}|{r['title']}>*"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "emoji": True,
                        "text": f"著者: {r['author']}\n{r['summary']}..."
                    }
                ]
            },
            {"type": "divider"}
        ])
        
    client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view={
            "type": "modal",
            # View identifier
            "callback_id": "view_more_papers",
            "title": {"type": "plain_text", "text": "Top10 AI Papers"},
            "blocks": sections
        }
    )
    
@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)

# アプリを起動します
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
    