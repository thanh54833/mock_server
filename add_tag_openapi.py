import json

# Load the Mockoon data
with open('mockoon/concung.json', 'r') as f:
    mockoon_data = json.load(f)

# Initialize the OpenAPI data
openapi_data = {
    "openapi": "3.0.0",
    "info": {
        "title": "API title",
        "version": "1.0.0"
    },
    "paths": {},
    "servers": [
        {
            "url": "http://10.10.11.159:3001/"
        }
    ],
}

# Convert the Mockoon data to OpenAPI format
for route in mockoon_data['routes']:
    path = "/" + route['endpoint']

    method = route['method'].lower()
    responses = {
        str(route['responses'][0]['statusCode']): {
            "description": "",
            "content": {
                "application/json": {
                    "example": route['responses'][0]['body']  # json.loads()
                }
            },
            "headers": {
                "Access-Control-Allow-Origin": {
                    "schema": {
                        "type": "string"
                    },
                    "example": "*"
                },
                "Access-Control-Allow-Methods": {
                    "schema": {
                        "type": "string"
                    },
                    "example": "GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS"
                },
                "Access-Control-Allow-Headers": {
                    "schema": {
                        "type": "string"
                    },
                    "example": "Content-Type, Origin, Accept, Authorization, Content-Length, X-Requested-With"
                },
                "": {
                    "schema": {
                        "type": "string"
                    },
                    "example": ""
                }
            }
        }
    }

    openapi_data['paths'][path] = {
        method: {
            "description": "",
            "responses": responses,
            "tags": [
                path.split("/")[1]
            ]
        }
    }

# Save the OpenAPI data
with open('openapi.json', 'w') as f:
    json.dump(openapi_data, f, indent=4)
