#!/bin/bash

config=$(cat config.yaml)
openai_org_id=$(echo "$config" | yq -r '.openai_org_id')
openai_api_key=$(echo "$config" | yq -r '.openai_api_key')

first_day_of_month=$(gdate +%Y-%m-01)
current_day=$(gdate +%Y-%m-%d)

prompt_token_cost=0.03
completion_token_cost=0.06

users=$(curl -s -H "method: GET" -H "authority: api.openai.com" -H "scheme: https" -H "path: /v1/organizations/$openai_org_id/users" -H "authorization: Bearer $openai_api_key" "https://api.openai.com/v1/organizations/$openai_org_id/users")

your_users=$(echo "$users" | jq '.members.data[].user | {id, name, email}')

while IFS= read -r row; do
  id_of_user=$(echo "$row" | jq -r '.id')
  total_context_tokens=0
  total_generated_tokens=0

  current_date="$first_day_of_month"
  while [[ "$current_date" < "$current_day" ]]; do
    user_data=$(curl -s -H "method: GET" -H "authority: api.openai.com" -H "authorization: Bearer $openai_api_key" -H "openai-organization: $openai_org_id" "https://api.openai.com/v1/usage?date=$current_date&user_public_id=$id_of_user")
    total_context_tokens=$((total_context_tokens + $(echo "$user_data" | jq '[.data[].n_context_tokens_total] | add')))
    total_generated_tokens=$((total_generated_tokens + $(echo "$user_data" | jq '[.data[].n_generated_tokens_total] | add')))
    current_date=$(gdate -d "$current_date + 1 day" +%Y-%m-%d)
  done

  email=$(echo "$row" | jq -r '.email')
  
  total_cost=$(echo "scale=2; ($total_context_tokens * $prompt_token_cost / 1000) + ($total_generated_tokens * $completion_token_cost / 1000)" | bc)
  
  user_json=$(echo "$row" | jq -c '. + {"usage": '"$user_data"', "total_cost": '"$total_cost"'}')

  user_name=$(echo "$row" | jq -r '.name' | tr ' ' '_')
  echo "$user_json" > "${user_name}.json"
done < <(echo "$your_users" | jq -c '.')