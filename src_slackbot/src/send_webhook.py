import os

import socket
from typing import Optional

from loguru import logger

from slack_sdk.webhook import WebhookClient
from slack_sdk.http_retry import (RetryHandler, RetryState, HttpRequest, HttpResponse)
from slack_sdk.http_retry.builtin_interval_calculators import BackoffRetryIntervalCalculator
from slack_sdk.http_retry.jitter import RandomJitter
from prepare.prepare_paper_data import call_paper_data_api

class MyRetryHandler(RetryHandler):
    def _can_retry(
        self,
        *,
        state: RetryState,
        request: HttpRequest,
        response: Optional[HttpResponse] = None,
        error: Optional[Exception] = None
    ) -> bool:
        # [Errno 104] Connection reset by peer
        return error is not None and isinstance(error, socket.error) and error.errno == 104



def send_webhook(text: str, blocks: list):
    url = os.getenv("SLACK_WEBHOOK_URL")
    logger.debug(f"SLACK_WEBHOOK_URL: {url}")
    
    webhook = WebhookClient(
        url=url,
        retry_handlers=[MyRetryHandler(
            max_retry_count=1,
            interval_calculator=BackoffRetryIntervalCalculator(
                backoff_factor=0.5,
                jitter=RandomJitter(),
            ),
        )],
    )

    response = webhook.send_dict({"text: ": text, "blocks": blocks})
    assert response.status_code == 200
    assert response.body == "ok"
    
def send_weekly_report():
    response = call_paper_data_api()
    
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
    
    send_webhook(
        text="今週のおすすめAI関連論文を紹介します！",
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
        ],
    )
    
    
# from crontab import CronTab

# if __name__ == '__main__':
#     cron = CronTab(user=True)
#     job = cron.new(command='python3 src_slackbot/src/webhook_handler/send_webhook.py')
#     job.minute.every(1)
#     cron.write()
    
if __name__ == "__main__":
    send_weekly_report()
    
    