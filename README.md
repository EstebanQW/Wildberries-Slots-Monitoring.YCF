# Для чего этот скрипт

Скрипт нужен для мониторинга доступности поставок с бесплатной приемкой на склады Wildberries. Каждые 15 минут (время указывается в настройках триггера) отправляет запрос на сервер Wildberries, получает дату в которые доступна поставка товара на склад. Если есть доступные слотоы с бесплатной приемкой, то на указанную почту отправляется письмо с уведомлением.

___

# Начало работы

* [Создание функции](#создание-функции)
* [Настройка триггера](#настройка-триггера)
* [Логика работы скрипта](#логика-работы-скрипта)
* [Запуск скрипта](#запуск-скрипта)
* [Остановка скрипта](#остановка-скрипта)
* [Работа скрипта](#работа-скрипта)
* [Изменение параметров (cookie, почта, номер заказа)](#изменение-параметров-cookie-почта-номер-заказа)
* [Где взять cookie](#где-взять-cookie)
* [Где взять номер заказа](#где-взять-номер-заказа)


## Создание функции

1. Необходимо создать функцию python на [Yandex Cloud Functions](https://console.yandex.cloud/folders) 
2. Заменить содержимое файла `index.py` в вашей функции на содержимое файла `index.py` из данного репозитория
3. Создать в функции 2 файла - `wb_calendar.py` и `requirements.txt`, вставить в них содержимое файлов `wb_calendar.py` и `requirements.txt` из данного репозитория (не забудьте вставить актуальные куки/почту/другие параметры в файл `lamoda_checker.py`)
4. В настройках функции установить таймаут 60 секунд и сохранить изменения
![image](https://github.com/user-attachments/assets/7b72ff96-543e-4886-9ad9-751239dee50f) 
5. Сделать функцию публичной переключив тумблер в обзоре функции
![image](https://github.com/user-attachments/assets/251ebed7-2ee7-4a82-87cb-db9e51597b18)


## Настройка триггера

Создать триггер, который будет запускать функцию каждые 15 минут (время на ваше усмотрение)
![image](https://github.com/user-attachments/assets/84fcbbf3-58c6-4e24-9e97-7a6b8b90fa14)



## Логика работы скрипта

Т.к. доступность приёмки на складе может отличаться в зависимости от количество поставляемых позиций, то для корректной работы необходимо создать поставку введя примерное количество поставляемых позиций. Скрипт будет мониторить склад, который мы выберем в момент создания поставки. Мониторинг будет происходить с текущей даты на месяц вперед (т.е. запустился сейчас 21.01.2025 17:26 - будет смотреть доступные слоты с 21.01.2025 17:26  до 21.02.2025 17:26. Следующий запуск через 15 минут, в 21.01.2025 17:41, будет смотреть до 21.02.2025 17:41 и т.д.)

Пример создания поставки для выбора склада и получения номера заказа:<br>
1.	Переходим на https://seller.wildberries.ru/supplies-management/all-supplies и жмем «Новая поставка»<br>
![image](https://github.com/user-attachments/assets/04d5f426-65e2-47ec-bcb4-b599e4da6b55)

2.	Выбираем «Выбрать из списка»<br>
![image](https://github.com/user-attachments/assets/432cb306-26e3-4115-a954-27852d5fe28c)

3.	Ставим галочку рядом с каким-нибудь товаром, вводим необходимое количество, и жмем кнопку «Применить»<br>
![image](https://github.com/user-attachments/assets/89050e94-6516-4b40-b184-92c21c97ece2)

4.	Жмем кнопку «Дальше»<br>
![image](https://github.com/user-attachments/assets/8e863c74-4b8c-4b43-8332-436e415bf4dd)

5.	Выбираем нужный склад (именно доступность поставок на этот склад будет мониторить скрипт)<br>
![image](https://github.com/user-attachments/assets/ab42fe44-12f2-48d9-b524-ea5b44e2af2f)

6.	Жмем «Дальше»<br>
![image](https://github.com/user-attachments/assets/71103127-5407-4c94-82b8-70222bd2dbef)

7.	Получаем номер заказа и список дат в которые доступна поставка на текущий момент:<br>
![image](https://github.com/user-attachments/assets/3bf995a1-6fe7-4440-a411-1946f2e94fb9)



## Запуск скрипта

Для запуска скрипта необходимо:<br>
1.	Зайти на https://console.yandex.cloud/folders/<br>
2.	Перейти в триггеры<br>
![image](https://github.com/user-attachments/assets/cf6dfbfe-1c27-4c67-b12b-1e3ca3b399fe)

3.	Кликнуть по триггеру<br>
![image](https://github.com/user-attachments/assets/47aba2d4-d174-4268-a4be-41e963a3876d)

4.	В правом верхнем углу нажать кнопку «Запустить»:<br>
![image](https://github.com/user-attachments/assets/e3190b37-10a5-406a-8d66-f213580ad39c)

Подтвердить действие:<br>
![image](https://github.com/user-attachments/assets/4282d3ba-5b60-4bb1-846c-704a2e29b575)

5.	Скрипт запущен (будет проверять доступность слотов каждые 15 минут и как только слоты станут доступны – слать письмо)

## Остановка скрипта

1.	Зайти на https://console.yandex.cloud/folders/<br>
2.	Перейти в триггеры<br>
![image](https://github.com/user-attachments/assets/b04f8ca5-f234-4621-a58a-dd24c3e5cb99)

3.	Кликнуть по триггеру<br>
![image](https://github.com/user-attachments/assets/a741cbb4-df95-4918-9c05-0220aef5323b)

4.	В правом верхнем углу нажать кнопку «Остановить»:<br>
![image](https://github.com/user-attachments/assets/4dea952c-4c04-4709-89f0-7cf4d1113139)

Подтвердить действие:<br>
![image](https://github.com/user-attachments/assets/c910249d-43c6-41ec-9970-5f861cc95b60)

5.	Скрипт остановлен

## Работа скрипта

При запущенном триггере скрипт будет запускаться каждые 15 минут и проверять на доступность слотов с бесплатной приёмкой.<br>
Когда слоты станут доступны скрипт отправляет письмо на почту.<br>
Пример: <br>
![image](https://github.com/user-attachments/assets/f8ea0737-4175-4699-8165-31c40eb9e427)

Если во время работы скрипта произошла какая-то ошибка, то скрипт отправит письмо с кодом ошибки.<br>
Пример:<br>
![image](https://github.com/user-attachments/assets/23778810-32ce-4827-b444-9b2af54d6019)



## Изменение параметров (cookie, почта, номер заказа)

1.	Зайти на https://console.yandex.cloud/folders/<br>
2.	Перейти в функции:<br>
![image](https://github.com/user-attachments/assets/acb876e3-b79a-403e-91de-18a09c311eec)

3.	Кликнуть по функции:<br>
![image](https://github.com/user-attachments/assets/5df0717d-1c6d-471d-81cf-d5922603db6b)

4.	Нажать на раздел «Редактор»:<br>
![image](https://github.com/user-attachments/assets/3fd72e22-cd34-43a0-8991-9696f0d30fe3)

5.	Перейти в файл `wb_calendar.py`<br>
![image](https://github.com/user-attachments/assets/2f44735e-e77d-4fff-9a91-6b2ed0ec43ce)

6.	Внести необходимые изменения в параметры:<br>
![image](https://github.com/user-attachments/assets/70f375c8-c48f-4175-8455-5698c39a9930)

7.	После внесения изменений пролистать вниз страницы и нажать на кнопку «Сохранить изменения»<br>
![image](https://github.com/user-attachments/assets/a3b478a1-4fad-43fd-a73c-cee4685b5d87)

8.	Изменения внесены

## Где взять cookie

1.	Зайти на https://seller.wildberries.ru/supplies-management/all-supplies <br>
2.	Нажать на клавиатуре «Ctrl+Shift+E» (если браузер фаерфокс)<br>
3.	Обновить страницу (F5)<br>
4.	Нажать на запрос, который начинается со слова `listSupplies`:<br>
![image](https://github.com/user-attachments/assets/4bd4fffb-c330-4796-b225-fcba648805cc)

5.	В меню справа во вкладке «Заголовки» пролистать до пункта «Заголовки запроса» и найти строку «Cookie»:<br>
![image](https://github.com/user-attachments/assets/329ff5b1-3635-4af5-97e6-4b3b51b65495)

6.	Нажать ПКМ по строке «Cookie» и нажать «Копировать значение»:<br>
![image](https://github.com/user-attachments/assets/dc37c6ce-e137-432e-98e3-a8648eff6a56)

7.	Скопированные cookie вставить в параметры (cookie обновляются примерно раз в сутки, поэтому при запущенном скрипте необходимо раз в сутки заходить, копировать новые cookie и вставлять их в параметры скрипта)

## Где взять номер заказа?

1.	Номер заказа можно найти на странице со всеми поставками <br>
![image](https://github.com/user-attachments/assets/b57c2428-e7f7-4ec2-8362-cd803ac0836a)


ИЛИ<br>


2.	После выбора склада в момент создания новой поставки:<br>
![image](https://github.com/user-attachments/assets/9e76ac6b-f568-4740-9d74-8f3f76e43fa1)

