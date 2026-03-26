import requests
import json

# Test the policy recommendation API
url = "http://127.0.0.1:5000/api/policy-recommend"
data = {
    "age": 30,
    "income": 500000,
    "driving_record": "Clean",
    "smoker": "No",
    "policy_type": "Health Insurance"
}

try:
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    print("Response:", response.text)
    
    if response.status_code == 200:
        result = response.json()
        print("\nSuccess:", result.get('success'))
        print("Risk Score:", result.get('risk_score'))
        print("\nRecommendation Preview:")
        recommendation = result.get('recommendation', '')
        print(recommendation[:500] + "..." if len(recommendation) > 500 else recommendation)
    else:
        print("Error:", response.text)
        
except requests.exceptions.ConnectionError:
    print("Error: Flask app is not running. Please start the Flask app first.")
except Exception as e:
    print("Error:", str(e))