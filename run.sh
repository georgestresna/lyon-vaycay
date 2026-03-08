#sudo systemctl start mongod
#echo "[*] Started MongoDB"
# sudo systemctl status mongod
docker compose -f 'docker-compose.yml' up -d --build 'selenium'

python3 ./app/main.py
echo "[*] Finished running, check trips_rated.json"

python3 ./web/web.py
echo "[*] Web server running at https://127.0.0.1:8000"

#sa dau drumu la dockercompose, si abia apoi pot sa folosesc seleniumu hybrid