URL_WEBHOOK = $(cat /root/env-url.txt)
echo $URL_WEBHOOK
cd ../app
CMD="$(pwd)"
echo $CMD

/usr/local/bin/python3 src/send_webhook.py $(cat /root/env-url.txt) 