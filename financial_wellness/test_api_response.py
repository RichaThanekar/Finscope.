import requests
import json

# Test the API endpoint
print("Testing Flask API endpoint...")
try:
    response = requests.get('http://127.0.0.1:5000/api/inflation-data', timeout=30)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nSuccess: {data.get('success')}")
        print(f"Latest Actual: {data.get('latest_actual')}")
        print(f"Avg Forecast: {data.get('avg_forecast')}")
        print(f"Trend: {data.get('trend')}")
        print(f"Data Points: {data.get('data_points')}")
        
        # Parse graph data
        if 'graph' in data:
            graph_data = json.loads(data['graph'])
            print(f"\nGraph has {len(graph_data['data'])} traces")
            
            for i, trace in enumerate(graph_data['data']):
                print(f"\nTrace {i}: {trace.get('name', 'Unnamed')}")
                if 'x' in trace:
                    x_data = trace['x']
                    y_data = trace['y']
                    print(f"  - Data points: {len(x_data) if isinstance(x_data, list) else 'N/A'}")
                    if isinstance(y_data, list) and len(y_data) > 0:
                        print(f"  - Y range: {min(y_data):.2f} to {max(y_data):.2f}")
                        print(f"  - First 3 Y values: {y_data[:3]}")
                        print(f"  - Last 3 Y values: {y_data[-3:]}")
        
        print("\n✅ API is working correctly!")
        
        # Check if values are linear
        if 'graph' in data:
            graph_data = json.loads(data['graph'])
            for trace in graph_data['data']:
                if trace.get('name') == 'Historical Inflation':
                    y_vals = trace['y']
                    if len(set([round(v, 1) for v in y_vals[:10]])) < 5:
                        print("\n⚠️ WARNING: Data appears to be linear/constant!")
                    else:
                        print("\n✓ Data has variation (not linear)")
    else:
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")
