import json
import requests
import datetime
from dateutil.relativedelta import relativedelta

# Read config.json
with open("config.json", "r") as f:
    config = json.load(f)

openai_org_id = config["openai_org_id"]
openai_api_key = config["openai_api_key"]

first_day_of_month = datetime.date.today().replace(day=1)
current_day = datetime.date.today()

prompt_token_cost = 0.03
completion_token_cost = 0.06

headers = {
    "method": "GET",
    "authority": "api.openai.com",
    "scheme": "https",
    "path": f"/v1/organizations/{openai_org_id}/users",
    "authorization": f"Bearer {openai_api_key}",
}

users_response = requests.get(f"https://api.openai.com/v1/organizations/{openai_org_id}/users", headers=headers)
users = users_response.json()["members"]["data"]

for user in users:
    id_of_user = user["user"]["id"]
    total_context_tokens = 0
    total_generated_tokens = 0

    daily_costs = {}  # Dictionary to store daily costs

    current_date = first_day_of_month
    while current_date <= current_day:
        usage_headers = {
            "method": "GET",
            "authority": "api.openai.com",
            "authorization": f"Bearer {openai_api_key}",
            "openai-organization": openai_org_id,
        }
        usage_response = requests.get(f"https://api.openai.com/v1/usage?date={current_date}&user_public_id={id_of_user}", headers=usage_headers)
        user_data = usage_response.json()

        context_tokens = sum([entry["n_context_tokens_total"] for entry in user_data["data"]])
        generated_tokens = sum([entry["n_generated_tokens_total"] for entry in user_data["data"]])
        total_context_tokens += context_tokens
        total_generated_tokens += generated_tokens

        # Calculate daily cost and store it in the dictionary
        daily_cost = (context_tokens * prompt_token_cost / 1000) + (generated_tokens * completion_token_cost / 1000)
        daily_costs[current_date.strftime("%Y-%m-%d")] = daily_cost

        current_date += relativedelta(days=1)

    email = user["user"]["email"]

    total_cost = (total_context_tokens * prompt_token_cost / 1000) + (total_generated_tokens * completion_token_cost / 1000)

    user_json = user["user"].copy()
    user_json["usage"] = user_data
    user_json["total_cost"] = total_cost
    user_json["daily_costs"] = daily_costs  # Add daily costs to the JSON

    user_name = user["user"]["name"].replace(" ", "_")
    with open(f"{user_name}.json", "w") as f:
        json.dump(user_json, f)