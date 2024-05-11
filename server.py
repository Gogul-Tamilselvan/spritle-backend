from flask import Flask, request, jsonify
from datetime import datetime
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType
from datadog_api_client.v2.model.metric_payload import MetricPayload
from datadog_api_client.v2.model.metric_point import MetricPoint
from datadog_api_client.v2.model.metric_resource import MetricResource
from datadog_api_client.v2.model.metric_series import MetricSeries

app = Flask(__name__)

@app.route('/submit_metrics', methods=['POST'])
def submit_metrics():
    try:
        # Parse request JSON
        data = request.get_json()

        configuration = Configuration(
        host="https://us5.datadoghq.com",)
        configuration.api_key['apiKeyAuth']='4012d6967e213f16da6e3c027e430014'
        configuration.api_key['appKeyAuth']='9560a294afc355c5cd06b3ec5cb00fc62d476bb9'
        
        for i in data['series']:
            print(i)
            body = MetricPayload(
                series=[
                    MetricSeries(
                        metric=i['metric'],
                        type=i['type'],
                        interval=i['interval'],
                        unit=i['unit'],
                        source_type_name="cjnjnj",
                        
                        points=[
                            MetricPoint(
                                timestamp=int(datetime.now().timestamp()),
                                value=0.7,
                            ),
                        ],
                        resources=[
                            MetricResource(
                                name="localhost",
                                type="host",
                            ),
                        ],
                        tags=["method:test","custom:metric"],
                    ),
                ],
            )
            print(body)
        # Submit metrics to Datadog
        with ApiClient(configuration) as api_client:
            api_instance = MetricsApi(api_client)
            response = api_instance.submit_metrics(body=body)

        # Serialize response to JSON-compatible dictionary
        response_dict = {
            "message": "Payload accepted",
            "response": response.to_dict()  # Convert response object to dictionary
        }

        return jsonify(response_dict), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)