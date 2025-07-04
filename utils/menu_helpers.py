from linebot.models import TextSendMessage, FlexSendMessage
import os

def choose_link():
    group = [
        "https://line.me/ti/p/g7TPO_lhAL",
        "https://line.me/ti/p/emkjaMQkMK",
        "https://line.me/ti/p/AKRUvSCLRC"
    ]
    return group[hash(os.urandom(8)) % len(group)]

def get_function_menu_flex():
    # 第一頁功能
    page1 = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {"type": "text", "text": "✨ 功能選單 1/2 ✨", "weight": "bold", "size": "lg", "align": "center", "color": "#C97CFD"},
                {"type": "separator"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "📱 驗證資訊", "text": "驗證資訊"},
                            "style": "primary",
                            "color": "#FFB6B6"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "uri",
                                "label": "📅 每日班表",
                                "uri": "https://t.me/+xLO-S74sdZMyYjA1"
                            },
                            "style": "secondary",
                            "color": "#FFF8B7"
                        },
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "🎁 每日抽獎", "text": "每日抽獎"},
                            "style": "primary",
                            "color": "#A3DEE6"
                        }
                    ]
                }
            ]
        }
    }
    # 第二頁功能
    page2 = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {"type": "text", "text": "✨ 功能選單 2/2 ✨", "weight": "bold", "size": "lg", "align": "center", "color": "#C97CFD"},
                {"type": "separator"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {"type": "uri", "label": "📬 預約諮詢", "uri": choose_link()},
                            "style": "primary",
                            "color": "#B889F2"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "uri",
                                "label": "🌸 茗殿討論區",
                                "uri": "https://line.me/ti/g2/mq8VqBIVupL1lsIXuAulnqZNz5vw7VKrVYjNDg?utm_source=invitation&utm_medium=link_copy&utm_campaign=default"
                            },
                            "style": "primary",
                            "color": "#FFDCFF"
                        }
                    ]
                }
            ]
        }
    }
    return FlexSendMessage(
        alt_text="功能選單",
        contents={
            "type": "carousel",
            "contents": [page1, page2]
        }
    )

def reply_with_menu(token, text=None):
    from extensions import line_bot_api
    msgs = []
    if text:
        msgs.append(TextSendMessage(text=text))
    msgs.append(get_function_menu_flex())
    line_bot_api.reply_message(token, msgs)
