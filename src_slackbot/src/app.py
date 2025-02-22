import os

from loguru import logger

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from prepare.prepare_paper_data import call_paper_data_api


# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# 'こんにちは' を含むメッセージをリッスンします
# 指定可能なリスナーのメソッド引数の一覧は以下のモジュールドキュメントを参考にしてください：
# https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
# 'こんにちは' を含むメッセージをリッスンします
@app.message("こんにちは")
def message_hello(message, say):
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"こんにちは、<@{message['user']}> さん！"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "クリックしてください"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"こんにちは、<@{message['user']}> さん！",
    )

@app.message("test")
def message_hello(message, say):
    response = call_paper_data_api()
    # logger.info(response)
    
    sections = []
    for r in response["datas"]:
        r['title'] = r['title'].replace('\n', '')
        r['summary'] = r['summary'][:40].replace('\n', '')
        sections.extend([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*<{r['id']}|{r['title']}>*\n{r['author']} (総被引用数: {r['citation_author']})\n"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Abstruct",
                            "emoji": True
                        },
                        "value": "show-more",
                        "action_id": "show-more"
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
                    "text": "今週のAI関連論文を紹介します！"
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

@app.action("button_click")
def action_button_click(body, ack, say):
    # アクションを確認したことを即時で応答します
    ack()
    # チャンネルにメッセージを投稿します
    say(f"<@{body['user']['id']}> さんがボタンをクリックしました！")
    
@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)

# アプリを起動します
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
    