import requests
import time
import datetime

# Получение айди игрока
player_id = input("Введите айди игрока: ")

# Настройки для ограничения количества запросов
MAX_REQUESTS_PER_MINUTE = 30
request_count = 0
last_request_time = datetime.datetime.now()

while True:
    # Выполнение запроса к API Opendota для получения списка матчей игрока
    player_matches_url = f"https://api.opendota.com/api/players/{player_id}/recentMatches"
    response = requests.get(player_matches_url)

    if response.status_code == 200:
        player_matches_data = response.json()

        # Извлечение значения match_id из каждого матча и выполнение POST-запроса
        for match in player_matches_data:
            match_id = match["match_id"]
            match_url = f"https://api.opendota.com/api/matches/{match_id}"
            match_response = requests.get(match_url)
            match_data = match_response.json()

            # Проверка, есть ли в матче чат
            if match_data.get("chat") is not None:
                print(f"Матч {match_id} содержит чат")
            else:
                request_url = f"https://api.opendota.com/api/request/{match_id}"
                response = requests.post(request_url)
                print(f"POST-запрос к {request_url} выполнен с кодом {response.status_code}")

            # Ограничение количества запросов
            request_count += 1
            if request_count >= MAX_REQUESTS_PER_MINUTE:
                elapsed_time = (datetime.datetime.now() - last_request_time).total_seconds()
                time_to_wait = 60 - elapsed_time
                if time_to_wait > 0:
                    print(f"Достигнуто ограничение количества запросов. Ждем {time_to_wait:.2f} секунд")
                    time.sleep(time_to_wait)
                request_count = 0
                last_request_time = datetime.datetime.now()
    else:
        print(f"Ошибка при выполнении запроса: {response.status_code}")
    
    # Ожидание 30 минут перед следующим запросом
    time.sleep(1800)
