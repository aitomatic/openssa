import requests

API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": "Can you please let us know more details about your ",
})
print(output)

output = query({
	"inputs": "What did I say?",
})
print(output)
