#!/bin/sh

crontab /var/spool/cron/crontabs/root

printenv SLACK_WEBHOOK_URL > /root/env-url.txt
service cron start

python src/app.py