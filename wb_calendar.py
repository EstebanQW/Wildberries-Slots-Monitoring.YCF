import json
import requests
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

#
#
#


cookie = "_"  # Куки
preorderID = 12345678  # Номер заказа
toaddr_list = [
    "example1@mail.ru",
    "example2@mail.ru",
]  # Адреса почты на которую слать письма

fromaddr = "example3@mail.ru"  # Почта с которой будут отправляться письма
mypass = "password"  # Пароль от почты для внешних приложений. Для mail.ru брать по ссылке - https://account.mail.ru/user/2-step-auth/passwords


#
#
#


# Узнаю dateFrom (текущая дата)
current_time = datetime.now(timezone.utc)
created_date_from = (
    current_time.strftime("%Y-%m-%dT%H:%M:%S.")
    + f"{current_time.microsecond // 1000:03d}Z"
)
dateFrom = created_date_from

# Узнаю dateTo (прибавляю к текущей дате 1 месяц)
new_time = current_time + relativedelta(months=1)
created_date_to = (
    new_time.strftime("%Y-%m-%dT%H:%M:%S.") + f"{new_time.microsecond // 1000:03d}Z"
)
dateTo = created_date_to


url = "https://seller-supply.wildberries.ru/ns/sm-supply/supply-manager/api/v1/supply/getAcceptanceCosts"

payload = json.dumps(
    {
        "params": {
            "dateFrom": dateFrom,
            "dateTo": dateTo,
            "preorderID": preorderID,
        },
        "jsonrpc": "2.0",
        "id": "json-rpc_58",
    }
)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "Referer": "https://seller.wildberries.ru/",
    "Origin": "https://seller.wildberries.ru",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Connection": "keep-alive",
    "Cookie": cookie,
}


def get_slots(response: requests.Response) -> None:
    find_error = False
    if response.status_code == 200:
        try:
            response_data = response.json()
            if "result" in response_data and "costs" in response_data["result"]:
                count = sum(
                    1
                    for item in response_data["result"]["costs"]
                    if item["coefficient"] == 0
                )
                print(f"Доступных слотов = {count}")
                if count > 0:
                    text_message = f"Появились доступные слоты WB с бесплатной приемкой. {count} шт. Мониторил заказ {preorderID}."
                    print(text_message)
                    print("Отправляю письмо.")
                    send_mail(find_error, text_message)
            else:
                find_error = True
                text_message = "Ответ не содержит ожидаемых данных. Необходимо проверить корректность preorderID или cookie."
                print(text_message)
                print("Отправляю письмо.")
                send_mail(find_error, text_message)
        except ValueError as e:
            find_error = True
            text_message = f"Ошибка при обработке ответа: {e}. Необходимо проверить корректность preorderID или cookie."
            print(text_message)
            print("Отправляю письмо.")
            send_mail(find_error, text_message)
    else:
        find_error = True
        text_message = f"Ошибка запроса, статус: {response.status_code}. Если код ошибки 403, то нужно поменять cookie в скрипте."
        print(text_message)
        print("Отправляю письмо.")
        send_mail(find_error, text_message)


def send_mail(find_error: bool, text_message: str) -> None:
    if find_error:
        # Тема для письма
        tema = "ОШИБКА ПОЛУЧЕНИЯ СЛОТОВ WB"
        # Тело для письма
        body = f"""<p>{text_message}</p>
        <br>
        <p><b>Все поставки:</b> <a href="https://seller.wildberries.ru/supplies-management/all-supplies">https://seller.wildberries.ru/supplies-management/all-supplies</a></p>"""
    else:
        # Тема для письма
        tema = "WB СТАЛИ ДОСТУПНЫ СЛОТЫ"
        # Тело для письма
        body = f"""<p><b>{text_message}</b></p>
        <br>
        <p><b>Все поставки:</b> <a href="https://seller.wildberries.ru/supplies-management/all-supplies">https://seller.wildberries.ru/supplies-management/all-supplies</a></p>"""

    msg = MIMEMultipart()
    msg["From"] = fromaddr
    msg["To"] = ", ".join(toaddr_list)
    msg["Subject"] = tema
    msg.attach(MIMEText(body, "html"))

    max_retries = 2  # количество попыток отправки email
    for _ in range(max_retries):
        try:
            server = smtplib.SMTP_SSL("smtp.mail.ru", 465)
            server.login(fromaddr, mypass)
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr_list, text)
            server.quit()
            print("Сообщение отправлено.")
            print("_____________________________________________")
            print()
            time.sleep(2)
            break
        except smtplib.SMTPException as e:
            print(f"Ошибка при отправке письма: {e}. Повторяю отправку...")
            time.sleep(2)
    else:
        print(f"Все попытки отправки письма не увенчались успехом. Ошибка.")
    time.sleep(1)


def main():
    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.text)
    get_slots(response)
