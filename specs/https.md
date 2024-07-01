## Local host:

1. Generate a self-signed SSL certificate:

```
openssl req -x509 -out localhost.crt -keyout localhost.key \
  -newkey rsa:2048 -nodes -sha256 \
  -subj '/CN=localhost' -extensions EXT -config <( \
   printf "[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")
```
2. Update your FastAPI application to use this certificate:
```
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# ... your routes here ...

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, ssl_keyfile='localhost.key', ssl_certfile='localhost.crt')
```
## public network:


1. brew install certbot
2. sudo certbot certonly --standalone -d concung.mock_server.vn
