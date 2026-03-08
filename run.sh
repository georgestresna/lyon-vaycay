sudo systemctl start mongod
echo "[*] Started MongoDB"
# sudo systemctl status mongod
python3 ./app/main.py
echo "[*] Finished running, check trips_rated.json"
python3 ./web/web.py
echo "[*] Web server running at https://127.0.0.1:8000"