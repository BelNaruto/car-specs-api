#!/usr/bin/env bash
# Car Specs API – cURL examples
# Get your key: https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/car-specs-api
# Support (fastest reply): Telegram @pintoflow
#
# Usage: RAPIDAPI_KEY=your_key bash examples.sh

set -euo pipefail
: "${RAPIDAPI_KEY:?Set RAPIDAPI_KEY first: export RAPIDAPI_KEY=your_key}"
HOST="car-specs-api.p.rapidapi.com"

call() {
  echo -e "\n=== $1 $2 ==="
  curl -sS -X "$1" "https://${HOST}$2" "${@:3}" \
    -H "x-rapidapi-host: ${HOST}" -H "x-rapidapi-key: ${RAPIDAPI_KEY}" | head -c 1200
  echo
}

call GET "/makes?year=2024"
call GET "/models?make=honda&year=2024&source=epa"
call GET "/trims?make=honda&model=civic&year=2024"
call GET "/specs/47069"
call GET "/vehicle?make=toyota&model=rav4&year=2021"
call GET "/mpg?make=tesla&model=model%203&year=2023"
call GET "/dimensions?make=toyota&model=rav4&year=2021"
call GET "/compare?ids=41189,47069"
call GET "/images?make=toyota&model=rav4&year=2021&limit=3"
call GET "/safety-ratings?make=toyota&model=rav4&year=2021"
call GET "/logo?make=toyota"
call GET "/search?q=2021%20toyota%20rav4"
call GET "/vin/decode?vin=1HGCM82633A004352"
call GET "/vin/specs?vin=1HGCM82633A004352"
call GET "/vin/validate?vin=1HGCM82633A004353"
call POST "/vin/batch" -H "content-type: application/json" -d '{"vins":["1HGCM82633A004352","5YJ3E1EA7KF317000"]}'
