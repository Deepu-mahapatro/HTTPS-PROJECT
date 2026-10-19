# 05. HTTPS Project Architecture

## 1. Architecture Overview

The architecture describes how the components of our HTTPS project communicate and work together.

Our project uses Postman as the client, TCP as the transport connection, TLS to secure communication, Uvicorn as the ASGI server, and FastAPI to process application requests.

The server runs locally at:

`https://localhost:8000`

Uvicorn is configured with a self-signed certificate and its corresponding private key.

## 2. Components and Their Responsibilities

| Component | Responsibility |
|---|---|
| Postman | Creates HTTPS requests and displays responses |
| TCP | Establishes the underlying network connection |
| TLS | Negotiates security and protects application data |
| Server certificate | Provides server identity information and a public key |
| Private key | Supports server authentication through cryptographic operations |
| Uvicorn | Handles TLS and HTTP communication and runs the ASGI application |
| FastAPI | Executes the matching endpoint and creates the response |
| Wireshark | Observes network packets exchanged between the client and server |

Each component has a specific role. TLS protects communication, while FastAPI focuses on application logic.

## 3. Step 1 — Start the HTTPS Server

We start Uvicorn from the project root using:

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --ssl-certfile certs/server.crt --ssl-keyfile certs/server.key
```

Uvicorn loads the certificate and private key, then listens for incoming connections on `127.0.0.1:8000`.

The application is available locally at:

`https://localhost:8000/`

The server remains running in the terminal while the client sends requests.

## 4. Step 2 — Postman Initiates the Request

In Postman, we send:

```http
GET https://localhost:8000/
```

Postman creates an HTTP request containing the method, path, headers, and any required body.

Because the URL uses `https://`, the client establishes a TLS connection before sending the HTTP request as protected application data.

The HTTP request is not sent as ordinary, unprotected HTTP over the network.

## 5. Step 3 — Establish TCP and TLS

The client first establishes a TCP connection to the server.

The TLS handshake then negotiates security parameters, exchanges key-share information, authenticates the server when certificate verification succeeds, and establishes traffic keys.

Our observed connection negotiated TLS 1.3 with the cipher suite `TLS_AES_256_GCM_SHA384` and the X25519 key-exchange group.

After the necessary handshake steps complete, the client and server can exchange TLS-protected application data.

## 6. Step 4 — Encrypt and Transmit the HTTP Request

Postman protects the HTTP request using the client-to-server TLS application traffic keys.

Conceptually, the request contains:

```http
GET / HTTP/1.1
Host: localhost:8000
```

The actual request is carried inside encrypted TLS records when transmitted over the network.

A network observer can generally see connection metadata, packet sizes, timing, and TLS record information, but cannot normally read the protected HTTP body or headers without the appropriate decryption secrets.

## 7. Step 5 — Uvicorn Receives and Decrypts the Request

Uvicorn receives the TLS records over the TCP connection.

Its TLS layer processes and decrypts the protected data, then reconstructs the HTTP request.

The resulting request is passed to the FastAPI application through the ASGI interface.

This is an important boundary:

- **On the network:** Application data is TLS-protected.
- **Inside the server:** Uvicorn makes the HTTP request available to FastAPI after TLS processing.

FastAPI does not need to decrypt TLS records itself.

## 8. Step 6 — FastAPI Processes the Request

Our `app/main.py` file defines the `/` endpoint:

```python
@app.get("/")
def home():
    return {
        "message": "HTTPS is working!",
        "project": "HTTPS-PROJECT",
        "status": "secure connection"
    }
```

FastAPI matches the request path and method to the endpoint, executes the function, and converts the returned Python dictionary into a JSON response.

At this stage, FastAPI is handling application logic rather than performing the TLS handshake.

## 9. Step 7 — Encrypt and Return the Response

The response travels back through the server:

1. FastAPI creates the JSON response.
2. Uvicorn receives the application response.
3. The TLS layer protects the HTTP response using the server-to-client application traffic keys.
4. The encrypted TLS records travel over the TCP connection.
5. Postman receives and decrypts the records.
6. Postman displays the HTTP response and JSON body.

The expected response body is:

```json
{
  "message": "HTTPS is working!",
  "project": "HTTPS-PROJECT",
  "status": "secure connection"
}
```

The existing TLS connection is normally reused for the response; a new handshake is not required for every response on that connection.

## 10. Complete Architecture Flow

```text
                    CLIENT
                 (Postman)
                     |
                     | HTTPS request
                     v
              TCP Connection
                     |
                     v
                TLS Handshake
                     |
                     | Establish traffic keys
                     v
           Encrypted HTTP Request
                     |
                     v
              Uvicorn TLS Layer
                     |
                     | Decrypt TLS records
                     v
              HTTP Request (ASGI)
                     |
                     v
              FastAPI Application
                  (main.py)
                     |
                     | Execute endpoint
                     v
                JSON Response
                     |
                     v
              Uvicorn TLS Layer
                     |
                     | Encrypt HTTP response
                     v
           Encrypted TLS Records
                     |
                     v
              TCP Connection
                     |
                     v
              Postman Response

        Wireshark observes network traffic
```

### Key Takeaways

- Postman initiates the HTTPS request, while TCP establishes the underlying connection.
- TLS establishes security and protects application data in transit.
- Uvicorn handles TLS and passes the decrypted HTTP request to FastAPI.
- FastAPI executes the endpoint and produces the JSON response.
- Uvicorn protects the response, and Postman decrypts and displays it.
- Wireshark observes network packets but does not automatically reveal encrypted application content.
