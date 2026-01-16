#!/bin/bash

BASE_URL="http://localhost:8000/api"
API_KEY="nnfn_dev_key"
URL_TO_ANALYZE="https://www.lemonde.fr/politique/article/2026/01/16/statut-de-la-nouvelle-caledonie-macron-veut-finir-son-mandat-sur-un-resultat-qui-se-derobe_6662480_823448.html"

echo "--- TEST 1: Requête sans clé ---"
curl -s -X POST "$BASE_URL/analyze" \
     -H "Content-Type: application/json" \
     -d "{\"url\": \"$URL_TO_ANALYZE\"}"
echo -e "\n"

echo "--- TEST 2: Requête avec clé invalide ---"
curl -s -X POST "$BASE_URL/analyze" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: wrong_key" \
     -d "{\"url\": \"$URL_TO_ANALYZE\"}"
echo -e "\n"

echo "--- TEST 3: Requête avec clé valide ---"
curl -s -X POST "$BASE_URL/analyze" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: $API_KEY" \
     -d "{\"url\": \"$URL_TO_ANALYZE\"}"
echo -e "\n"

echo -e "\n--- TEST 4: Test du Rate Limit (5 req/min) ---"
for i in {1..6}
do
   echo "Tentative $i..."
   curl -s -o /dev/null -w "%{http_code}\n" -X POST "$BASE_URL/analyze" \
        -H "Content-Type: application/json" \
        -H "X-API-Key: $API_KEY" \
        -d "{\"url\": \"$URL_TO_ANALYZE\"}"
done
