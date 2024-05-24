docker run -d -p 8081:8080 -e SWAGGER_JSON=/mnt/openapi.json -v /Users/phamthanh/Desktop/openapi.json:/mnt/openapi.json
--name cc_swagger swaggerapi/swagger-ui

tags:

- name: pet
  description: Everything about your Pets
  externalDocs:
  description: Find out more
  url: http://swagger.io
- name: store
  description: Access to Petstore orders
  externalDocs:
  description: Find out more about our store
  url: http://swagger.io
- name: user
  description: Operations about usern