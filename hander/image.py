\\\from linebot.models import MessageEvent, ImageMessage, TextSendMessage
from app import handler, line_bot_api
from utils.image_verification import extract_lineid_phone
from utils.special_case import is_special_case
from app import temp_users
import os

@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    user_id = event.source.user_id
    if user_id not in temp_users or temp_users[user_id].get("step") != "waiting_screenshot":
        return

    if is_special_case(user_id):
        record = temp_users[user_id]
        reply = (
            f"📱 {record['phone']}\n"
            f"🌸 暱稱：{record['name']}\n"
            f"       個人編號：待驗證後產生\n"
            f"🔗 LINE ID：{record['line_id']}\n"
            f"（此用戶經手動通過）\n"
            f"請問以上資料是否正確？正確請回復 1\n"
            f"⚠️輸入錯誤請從新輸入手機號碼即可⚠️"
        )
        record["step"] = "waiting_confirm"
        temp_users[user_id] = record
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
        return

    message_content = line_bot_api.get_message_content(event.message.id)
    image_path = f"/tmp/{user_id}_line_profile.png"
    with open(image_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

    phone_ocr, lineid_ocr, ocr_text = extract_lineid_phone(image_path)
    os.remove(image_path)
    input_phone = temp_users[user_id].get("phone")
    input_lineid = temp_users[user_id].get("line_id")
    record = temp_users[user_id]

    if input_lineid == "尚未設定":
        if phone_ocr == input_phone:
            reply = (
                f"📱 {record['phone']}\n"
                f"🌸 暱稱：{record['name']}\n"
                f"       個人編號：待驗證後產生\n"
                f"🔗 LINE ID：尚未設定\n"
                f"請問以上資料是否正確？正確請回復 1\n"
                f"⚠️輸入錯誤請從新輸入手機號碼即可⚠️"
            )
            record["step"] = "waiting_confirm"
            temp_users[user_id] = record
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="❌ 截圖中的手機號碼與您輸入的不符，請重新上傳正確的 LINE 個人頁面截圖。")
            )
    else:
        lineid_match = (lineid_ocr is not None and input_lineid is not None and lineid_ocr.lower() == input_lineid.lower())
        if phone_ocr == input_phone and (lineid_match or lineid_ocr == "尚未設定"):
            reply = (
                f"📱 {record['phone']}\n"
                f"🌸 暱稱：{record['name']}\n"
                f"       個人編號：待驗證後產生\n"
                f"🔗 LINE ID：{record['line_id']}\n"
                f"請問以上資料是否正確？正確請回復 1\n"
                f"⚠️輸入錯誤請從新輸入手機號碼即可⚠️"
            )
            record["step"] = "waiting_confirm"
            temp_users[user_id] = record
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text=(
                        "❌ 截圖中的手機號碼或 LINE ID 與您輸入的不符，請重新上傳正確的 LINE 個人頁面截圖。\n"
                        f"【圖片偵測結果】手機:{phone_ocr or '未識別'}\nLINE ID:{lineid_ocr or '未識別'}"
                    )
                )
            )