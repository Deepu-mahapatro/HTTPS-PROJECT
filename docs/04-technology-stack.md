# 04. HTTPS Project — Technology Stack

## 1. Technology Stack Overview

A technology stack is the collection of programming languages, frameworks, servers, tools, and services used to build and test an application.

In this project, we combined Python and FastAPI to build the API, Uvicorn to run it over HTTPS, OpenSSL to generate the local certificate, and testing tools to inspect the communication.

Each technology has a different responsibility. Together, they help us understand the complete HTTPS flow.

## 2. Python

**What it is:** Python is the programming language used to implement our application.

**Purpose:** It allows us to define endpoints, execute application logic, and generate responses.

In our project, `app/main.py` contains the Python code for our FastAPI application.

Example:

```python
@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

When a request reaches `/health`, this function returns a Python dictionary that FastAPI converts into a JSON response.

## 3. FastAPI

**What it is:** FastAPI is a Python web framework for building APIs.

**Purpose:** It defines routes, handles application-level requests, and produces responses.

Our application is created in `app/main.py`:

```python
from fastapi import FastAPI

app = FastAPI(title="HTTPS Learning Project")
```

We defined two endpoints:

- `/` — returns the project message.
- `/health` — returns the application's health status.

FastAPI handles the application logic. In our setup, it does not directly manage the TLS handshake or encrypt every HTTP response.

## 4. Uvicorn

**What it is:** Uvicorn is an ASGI server that runs Python web applications, including FastAPI.

**Purpose:** It accepts network connections, handles HTTP communication, and can provide TLS when configured with a certificate and private key.

We start the project with:

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --ssl-certfile certs/server.crt --ssl-keyfile certs/server.key
```

Here:

- `app.main:app` identifies the FastAPI application object.
- `127.0.0.1` restricts the server to the local machine.
- `8000` is the listening port.
- `--ssl-certfile` specifies the server certificate.
- `--ssl-keyfile` specifies the corresponding private key.

Uvicorn handles TLS in this configuration and passes decrypted HTTP requests to FastAPI.

## 5. OpenSSL

**What it is:** OpenSSL is a cryptographic toolkit that provides TLS-related tools and cryptographic functionality.

**Purpose in our project:** We used it to generate and inspect the local certificate and private key and to inspect a TLS connection.

Our certificate-generation command was:

```powershell
openssl req -x509 -newkey rsa:2048 -sha256 -days 365 -nodes -keyout certs/server.key -out certs/server.crt -subj "/CN=localhost" -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
```

This creates a self-signed certificate and its corresponding private key.

The certificate is valid for the configured `localhost` and `127.0.0.1` names, subject to the client's certificate validation rules.

OpenSSL is a separate tool from FastAPI. Generating the certificate does not automatically configure Uvicorn; we explicitly provide the file paths when starting the server.

## 6. Server Certificate and Private Key

The certificate and private key form an important part of our local HTTPS setup.

| File | Purpose |
|---|---|
| `certs/server.crt` | Contains certificate information and the server's public key |
| `certs/server.key` | Contains the corresponding private key |

The certificate can be shared, but the private key must remain secret.

Our certificate is self-signed, meaning it was not issued by a publicly trusted certificate authority. A client must explicitly trust it or otherwise configure validation appropriately to establish trusted server identity.

Neither file is generated for every HTTP request. Uvicorn loads them to configure the HTTPS listener.

## 7. Postman

**What it is:** Postman is an API testing tool.

**Purpose:** It allows us to send HTTP and HTTPS requests, inspect status codes, view headers, and read response bodies.

We tested our local endpoint:

`https://localhost:8000/`

The expected response contains:

```json
{
  "message": "HTTPS is working!",
  "project": "HTTPS-PROJECT",
  "status": "secure connection"
}
```

Postman also helped us encounter and investigate the trust warning caused by our self-signed certificate.

A successful response alone does not prove that certificate verification was enabled. Certificate trust must be checked separately.

## 8. curl and Wireshark

### curl

`curl` is a command-line tool for making network requests.

We used:

```powershell
curl.exe -k https://localhost:8000/
```

The `-k` option skips certificate verification. It is useful for local testing with a self-signed certificate, but it must not be used as a production security practice.

### Wireshark

Wireshark captures and inspects network packets.

We captured loopback traffic and used this display filter:

```text
tcp.port == 8000
```

For TLS handshake messages, we used:

```text
tcp.port == 8000 && tls.handshake
```

Wireshark helps us observe connection metadata and TLS records. In TLS 1.3, many handshake messages after ServerHello are encrypted, so their contents may not be visible in an ordinary capture.

## 9. VS Code, PowerShell, Git, and GitHub

- **VS Code:** Used to edit the Python application, configuration files, and documentation.
- **PowerShell:** Used to run commands, start Uvicorn, and execute tests on Windows.
- **Git:** Tracks changes and records project versions through commits.
- **GitHub:** Hosts the repository so the source code and documentation can be shared.

We exclude the local certificate, private key, virtual environment, and other sensitive or generated files from Git tracking.

The private key must never be committed to the repository.

## 10. How the Technologies Work Together

The technologies form the following workflow:

```text
OpenSSL
   |
   | Generates local certificate and private key
   v
Uvicorn <---------------- Postman / curl
   |                          |
   | TLS and HTTP             | HTTPS request
   v                          |
FastAPI <---------------------+
   |
   | Application response
   v
Uvicorn
   |
   | TLS-protected response
   v
Postman / curl

Wireshark observes network packets.
VS Code and PowerShell support development and testing.
Git tracks project changes; GitHub hosts the repository.
```

### Key Takeaways

- Python and FastAPI implement the application logic.
- Uvicorn runs the application and provides TLS in our current configuration.
- OpenSSL generates and inspects cryptographic material and TLS connections.
- Postman and curl test the API, while Wireshark inspects network traffic.
- Git and GitHub support version control and project sharing.
- The self-signed certificate is for local learning; production HTTPS requires appropriate certificate validation and secure key management.
