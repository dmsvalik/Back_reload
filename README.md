
#### Django API.
# Project - Marketplace Tumen

<img src="https://github.com/ERAalex/new_test/blob/main/marketplace.png">

<br><a href="mailto:service000market@gmail.com"><img src="https://img.shields.io/badge/-Gmail%20contact%20us-red"></a>
<br><a href="#"><img src="https://img.shields.io/badge/-Telegram-blue"></a>

## About the project.

  <a href="#" target="_blank" rel="noreferrer nofollow">
    <img src="https://github.com/ERAalex/new_test/blob/main/website_icons.jpg" >
  </a>

This project is under development.<br>

### Важные моменты.

- Работаем над API.
- Подключен Swagger для удобства просмотра документации проекта.<br>
наберите http://127.0.0.1:8000/swagger/  или http://127.0.0.1:8000/redoc/ <br>
- Настроен Debug Toolbar

<br>
<br>

### Работа с ветками.

Проект содержит основую ветку main. Она предназначена для деплоя. В нее не пушим и не мержим. <br>
Ветка pre-main предназначена для слияния рабочих веток.<br>
Для новой работы (баги, фиксы, фичи...) ответвляемся от ветки pre-main и называем ветку fix/"имя вашей ветки".<br>
Варианты названий веток в зависимости от реализуемой логики:<br><br>

- fix/      - изменение какого-то бага<br>
- feat/   - новые фишки проекта, новый код<br>
- ref/     - рефакторинг кода, улучшение<br>
- tech/ - технические моменты проекта. например добавление Celery и т.д.<br>
- chore/  - для всего остального (writing documentation, formatting, adding tests, cleaning useless code etc.)<br>

После завершения работы делаем MR в ветку pre-main и ждем одобрения.<br>
Не забывайте менять статус работы в Kaiten.

<br>
<br>

### Наши разработчики.


<br><br>



## 1. Подготовка к запуску проекта <a id="preparation"></a>

- Скачайте репозиторий.
```shell
git clone https://github.com/TyuMeb/Back_reload.git -b pre-main
```

- Установите зависимости.
```shell
pip install -r requirements.txt
```


- Настройка переменных окружения. Перед запуском проекта необходимо создать файл
```.env``` в директории `config`.
> **внимание**: Если нужны данные (пароли) обратитесь к Alex R_.

```shell
[settings]

SECRET_KEY =
DEBUG_STATUS =

[database]

DB_ENGINE =
DB_NAME =
DB_PASS =
DB_USER =
DB_HOST =
DB_PORT =

[email_host]

EMAIL_HOST =
EMAIL_HOST_USER =
EMAIL_HOST_PASSWORD =
EMAIL_PORT =
EMAIL_USE_TLS =
```
БД можно развернуть как в Docker, так и локально. (рекоменудуем создать локально)

- Проведите первые миграции и запустите проект

```shell
python manage.py migrate
```


### 2. Правила по созданию веток и pull request
Вся работа проходит с веткой pre-main. Как только набирается критическая масса обновлений DevOps(Ильшат) или Team Lead
проводят мерж с главной веткой (main), которая связана с CI/CD Jenkins. <br> <br>
Ваши шаги:
- Выберите ticket или tasks на Kaiten доске.
- Отметьте на доске Kaiten, что Вы взяли в работу task (Обязательно поставьте
ориентировочные сроки выполнения задачи)
- Создайте ветку с следующим названием: task/описание проблемы
> **пример**: ```git checkout -b task/fix_model_User_problem```
старайтесь часто делать commits и указывать в них основную суть проделанной работы (предпочтительно на
> английском)
- Как только Вы решили проблему и готовы ее отправить на проверку наберите команду
> **Примечание**: использование Poetry и pre-commit при работе над проектом очень рекомендуется. Спасибо.

```shell
git push origin task/fix_model_User_problem
```
- Создайте pull request к ветке pre-main , ждите проверки кода.

### 3.1 Рекомендации. Poetry<a id="poetry"></a>
Poetry - инструмент для управления зависимостями и виртуальными окружениями, также может использоваться для сборки
пакетов.

- <details>
    <summary>
      Как скачать и установить?
    </summary>

  - Установите poetry следуя [инструкции с официального сайта](https://python-poetry.org/docs/#installation).
  - <details>
      <summary>
      Команды для установки
      </summary>

      > Для UNIX-систем и Bash on Windows вводим в консоль следующую команду:
      > ```shell
      > curl -sSL https://install.python-poetry.org | python -
      > ```
      >
      > Для WINDOWS PowerShell:
      > ```shell
      > (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
      > ```
    </details>
    <br>

  - После установки - перезапустите оболочку и введите команду:
    ```shell
    poetry --version
    ```

    Если установка прошла успешно, вы получите ответ в формате `Poetry (version 1.3.2)`

  - Для дальнейшей работы создайте виртуальное окружение:
    ```shell
    poetry config virtualenvs.in-project true
    poetry install
    ```
    Результатом выполнения команды станет создание в корне проекта папки .venv.
    Зависимости для создания окружения берутся из файлов poetry.lock (приоритетнее) и pyproject.toml

  - Для добавления новой зависимости в окружение необходимо выполнить команду
    ```shell
    poetry add <package_name>
    ```

  - Также poetry позволяет разделять зависимости необходимые для разработки, от основных.
    Для добавления зависимости необходимой для разработки и тестирования необходимо добавить флаг `--group dev`
    ```shell
    poetry add <package_name> --group dev
    ```
</details>

- <details>
    <summary>
      Порядок работы после настройки
    </summary>

    <br>

  - Чтобы активировать виртуальное окружение, введите команду:
    ```shell
    poetry shell
    ```

  - Доступен стандартный метод работы с активацией окружения в терминале.

</details>

### 3.2. Pre-commit <a id="pre-commit"></a>
Pre-commit - инструмент автоматического запуска различных проверок перед выполнением коммита.

Установите pre-commit командой:
```shell
pre-commit install
```
Теперь при каждом коммите у вас будет автоматическая проверка линтером,
а так же, автоматическое форматирование кода.


## 4. Тестирование
Для тестирования используется **_pytest_** в связке с **_pytest-django_**. Все тесты размещены в папке `tests`,
в корне репозитория.

### 4.1. Дополнительная информация

Запуск всех тестов:
```shell
pytest
```

Запуск отдельной группы тестов:
```shell
pytest -m users
```
> На данный момент есть только одна группа `users`
> При необходимости, с помощью декоратора `@pytest.mark.now` можно выбрать тесты, над которыми ведётся работа в
> данный момент, и запускать их командой: `pytest -m now`

<br>
<br>
<br>
