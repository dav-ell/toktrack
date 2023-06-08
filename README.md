# toktrack
Scripts to monitor your organization's OpenAI API token usage and cost per user.

Usage:
 1. `git clone https://github.com/dav-ell/toktrack.git`
 2. Get your organization ID from here: https://platform.openai.com/account/org-settings
 3. Get your API key from here: https://platform.openai.com/account/api-keys
 4. Put those in the `config.json` file.
 5. Run `python3 get_openai_usage.py`
 6. A JSON file will be created for each user in your organization, with contents like this:

```json
{
    "object": "user",
    "id": "user-<id>",
    "name": "<name>",
    "email": "<email>",
    "picture": "<url>",
    "usage": {
        "object": "list",
        "data": [
            {
                "aggregation_timestamp": "<timestamp>",
                "n_requests": 1,
                "operation": "completion",
                "snapshot_id": "gpt-4-0314",
                "n_context": 1,
                "n_context_tokens_total": 1584,
                "n_generated": 1,
                "n_generated_tokens_total": 156
            },
            {
                "aggregation_timestamp": "<timestamp>",
                "n_requests": 1,
                "operation": "completion",
                "snapshot_id": "gpt-4-0314",
                "n_context": 1,
                "n_context_tokens_total": 1638,
                "n_generated": 1,
                "n_generated_tokens_total": 458
            },
            {
                "aggregation_timestamp": "<timestamp>",
                "n_requests": 1,
                "operation": "completion",
                "snapshot_id": "gpt-4-0314",
                "n_context": 1,
                "n_context_tokens_total": 415,
                "n_generated": 1,
                "n_generated_tokens_total": 287
            }
        ],
        "ft_data": [],
        "dalle_api_data": [],
        "whisper_api_data": [],
        "current_usage_usd": 0.0
    },
    "total_cost": 1.8453899999999999,
    "daily_costs": {
        "2023-06-01": 0.68382,
        "2023-06-02": 0.06273,
        "2023-06-03": 0.053279999999999994,
        "2023-06-04": 0.0,
        "2023-06-05": 0.13208999999999999,
        "2023-06-06": 0.7503,
        "2023-06-07": 0.16316999999999998
    }
}
```