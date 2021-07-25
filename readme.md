# Выгрузка информации для сайта

## Виды выгрузок

- Дома `rep_ivc_buildings @tip_id=:tip_id, @build_id=:build_id, @format=:format`
- Помещения `rep_ivc_flats @tip_id=:tip_id, @build_id=:build_id, @format=:format`
- Лицевые счета  `rep_ivc_occ @tip_id=:tip_id, @fin_id=:fin_id, @build_id=:build_id, @debug=0, @format=:format`
- Жители `rep_ivc_people @fin_id=:fin_id, @tip_id=:tip_id, @build_id=:build_id, @format=:format`
- Регистрация граждан `rep_ivc_people_period @fin_id=:fin_id, @tip_id=:tip_id, @build_id=:build_id, @format=:format`
- Счетчики (ПУ)  `rep_ivc_counter @tip_id=:tip_id, @build_id=:build_id, @format=:format`
- Показания ПУ  `rep_ivc_counter_value @fin_id=:fin_id, @tip_id=:tip_id, @build_id=:build_id, @format=:format`
- Начисления  `rep_ivc_value @fin_id=:fin_id, @tip_id=:tip_id, @build_id=:build_id, @format=:format`
- Оплаты  `rep_ivc_pay @fin_id=:fin_id, @tip_id=:tip_id, @build_id=:build_id, @sup_id=:sup_id, @format=:format`
- Долги  `rep_ivc_dolg @fin_id=:fin_id,@tip_str=:tip_str,@sup_id=:sup_id, @build_id=:build_id, @only_dolg=0, @format=:format`
- Квитанции  `rep_ivc_pd @fin_id=:fin_id, @tip_id=:tip_id, @build_id=:build_id, @sup_id=:sup_id, @format=:format`

## запуск виртуального окружения

windows: `source venv/Scripts/activate`
linux: `source venv/bin/activate`

## запуск сервиса

uvicorn backend.buffer.main:app --reload --port=8001

## тестирование

>pytest -vx  
>pytest -v backend/tests/test_api_pd.py -s

## Команды по docker

docker-compose up --build
docker-compose up

docker build -t puzanovma/fastapi-buffer -f ./backend/Dockerfile .
docker run -d -p 8001:8001 --name buffer-container  puzanovma/fastapi-buffer 

docker rm -vf $(docker ps -a -q)
docker rmi $(docker images -f dangling=true -q)

curl 127.0.0.1:8001

# Запуск тестов в Linux
pytest-3