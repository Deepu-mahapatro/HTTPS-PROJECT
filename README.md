# 🔐 HTTPS Learning Project

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Uvicorn-ASGI_Server-4051B5?style=for-the-badge" alt="Uvicorn">
  <img src="https://img.shields.io/badge/TLS-1.3-2E8B57?style=for-the-badge" alt="TLS 1.3">
  <img src="https://img.shields.io/badge/OpenSSL-Cryptography-721412?style=for-the-badge&logo=openssl&logoColor=white" alt="OpenSSL">
  <img src="https://img.shields.io/badge/Postman-API_Testing-FF6C37?style=for-the-badge&logo=postman&logoColor=white" alt="Postman">
  <img src="https://img.shields.io/badge/Wireshark-Packet_Analysis-1679A7?style=for-the-badge&logo=wireshark&logoColor=white" alt="Wireshark">
</p>

<p align="center">
  <b>A hands-on project for understanding HTTPS, TLS 1.3, certificate verification, key establishment, and encrypted HTTP communication using FastAPI and Uvicorn.</b>
</p>

---

## 1. 📌 Project Overview

This project demonstrates how HTTPS protects communication between a client and a web server using TLS (Transport Layer Security).

We built a FastAPI application and configured Uvicorn to serve it over HTTPS using a locally generated, self-signed certificate and its corresponding private key.

The project focuses on understanding the complete process, from establishing a TCP connection and performing the TLS handshake to sending an encrypted HTTP request and receiving the response.

## 2. 🎯 Project Objectives

- Understand HTTP versus HTTPS.
- Learn the purpose of TLS and the TLS 1.3 handshake.
- Understand server certificates and private keys.
- Learn how shared secrets and traffic keys are established.
- Configure HTTPS for a FastAPI application using Uvicorn.
- Test HTTPS endpoints using Postman, curl, and OpenSSL.
- Inspect TLS handshake traffic using Wireshark.
- Trace the complete request-to-response flow.
- Understand the differences between encrypted communication and trusted server identity.

---

## 3. 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | Defines API endpoints and application logic |
| Uvicorn | Runs FastAPI and handles TLS in our configuration |
| OpenSSL | Generates and inspects the local certificate and private key |
| Postman | Sends HTTPS requests and displays responses |
| curl | Tests endpoints from the terminal |
| Wireshark | Captures and inspects network packets |
| VS Code | Development environment |
| Git and GitHub | Version control and repository hosting |

---

## 4. 🏗️ Project Architecture

```text
                 CLIENT
             Postman / curl
                    |
                    | HTTPS request
                    v
              TCP Connection
                    |
                    v
              TLS Handshake
                    |
                    | Secure connection established
                    v
          Encrypted HTTP Request
                    |
                    v
             Uvicorn TLS Layer
                    |
                    | Decrypt request
                    v
             FastAPI Application
                 (main.py)
                    |
                    | Process endpoint
                    v
              JSON Response
                    |
                    v
             Uvicorn TLS Layer
                    |
                    | Encrypt response
                    v
          Encrypted TLS Records
                    |
                    v
             Postman / curl

       Wireshark observes network traffic
```

### Core Principle

> TLS protects HTTP communication in transit. Uvicorn handles TLS, while FastAPI processes the application request and generates the response.

---

## 5. ⚡ Features Implemented

| Feature | Description |
|---|---|
| FastAPI application | Defines the API endpoints |
| Home endpoint | Returns the project message |
| Health endpoint | Returns the application health status |
| Local HTTPS | Configures Uvicorn with a TLS certificate and private key |
| Self-signed certificate | Enables local HTTPS testing |
| TLS inspection | Inspects the negotiated TLS connection using OpenSSL |
| API testing | Sends HTTPS requests using Postman and curl |
| Packet inspection | Observes TCP and TLS traffic using Wireshark |
| Handshake learning | Studies TLS negotiation, certificate authentication, and key establishment |
| Documentation | Explains the HTTPS concepts, technology stack, and architecture |

---

## 6. 🌐 Endpoints and Testing

The local HTTPS base URL is:

```text
https://localhost:8000
```

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Returns the project message |
| GET | `/health` | Checks application health |

### Example response

```json
{
  "message": "HTTPS is working!",
  "project": "HTTPS-PROJECT",
  "status": "secure connection"
}
```

### Test with curl

```powershell
curl.exe -k https://localhost:8000/
```

The `-k` option skips certificate verification. It is used here only for local testing with the self-signed certificate; it must not be used as a production security practice.

### Inspect the TLS connection

```powershell
openssl s_client -connect localhost:8000 -servername localhost
```

This command can display the negotiated TLS protocol, cipher suite, and certificate verification result.

---

## 7. 🔐 How HTTPS Works

HTTPS is HTTP communication protected by TLS.

The overall process is:

1. The client establishes a TCP connection.
2. The client and server exchange TLS handshake messages.
3. The server provides its certificate and proves possession of the corresponding private key in a certificate-authenticated handshake.
4. The client validates the certificate according to its trust configuration.
5. Both sides establish shared secret material and derive traffic keys.
6. The client sends the HTTP request through TLS.
7. Uvicorn decrypts the request and passes it to FastAPI.
8. FastAPI processes the endpoint and creates the response.
9. Uvicorn encrypts the response, and the client decrypts and displays it.

### TLS 1.3 handshake overview

```text
Client                          Server
  |                                |
  |-------- ClientHello ---------->|
  |<------- ServerHello -----------|
  |                                |
  |    Key establishment           |
  |                                |
  |<-- Encrypted handshake --------|
  |                                |
  |-------- Finished ------------->|
  |                                |
  |   Encrypted HTTP request       |
  |------------------------------->|
  |                                |
  |<------ HTTP response ----------|
```

This is a simplified view of a typical full TLS 1.3 handshake. Exact messages and ordering can vary.

---

## 8. 🧪 Verification and Observations

We used different tools to examine different parts of the connection.

| Tool | What it helps verify |
|---|---|
| Postman | HTTPS requests and application responses |
| curl | Endpoint response from the terminal |
| OpenSSL | Negotiated TLS parameters and certificate verification result |
| Wireshark | TCP packets, ClientHello, ServerHello, and TLS records |

Our connection test negotiated TLS 1.3 with the cipher suite `TLS_AES_256_GCM_SHA384` and the X25519 key-exchange group.

The certificate is self-signed, so certificate verification can report a trust error even when TLS encryption has been negotiated. A successful request made with verification disabled does not prove that the certificate is trusted.

Wireshark can show TLS record metadata, but many TLS 1.3 handshake messages after ServerHello and the application data are encrypted in an ordinary capture.

---

## 9. 📁 Project Structure and Documentation

```text
HTTPS-PROJECT/
│
├── app/
│   ├── __init__.py
│   └── main.py
│
├── certs/                    # Local files; excluded from Git
│   ├── server.crt
│   └── server.key
│
├── docs/
│   ├── 01-project-overview.md
│   ├── 02-https-end-to-end.md
│   ├── 03-tls-handshake.md
│   ├── 04-technology-stack.md
│   └── 05-architecture.md
│
├── .gitignore
├── requirements.txt
└── README.md
```

The virtual environment (`venv/` or `.venv/`) exists locally but is excluded from Git.

### Documentation files

| Document | What it covers |
|---|---|
| [Project Overview](docs/01-project-overview.md) | Project purpose, objectives, and scope |
| [HTTPS End-to-End](docs/02-https-end-to-end.md) | How HTTPS protects communication |
| [TLS Handshake](docs/03-tls-handshake.md) | Certificate authentication, key exchange, and traffic-key derivation |
| [Technology Stack](docs/04-technology-stack.md) | Tools used and their responsibilities |
| [Architecture](docs/05-architecture.md) | Complete client-to-server request and response flow |

---

## 10. 🚀 Setup, Security, and Learning Outcomes

### Prerequisites

- Python 3.12 or a compatible Python version.
- OpenSSL for generating the local certificate.
- Git for version control.

### Install dependencies

Open PowerShell in the project root:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Generate a local certificate

If you have not already generated the certificate, create the `certs` directory and run this command from the project root:

```powershell
New-Item -ItemType Directory -Force certs
openssl req -x509 -newkey rsa:2048 -sha256 -days 365 -nodes -keyout certs/server.key -out certs/server.crt -subj "/CN=localhost" -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
```

This assumes OpenSSL is available in your `PATH`. If it is not, use the full path to your OpenSSL executable.

### Start the HTTPS server

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --ssl-certfile certs/server.crt --ssl-keyfile certs/server.key
```

Open `https://localhost:8000/` in Postman or test it with curl.

### Security notes

- The certificate is self-signed and intended for local learning.
- Keep `certs/server.key` secret and excluded from GitHub.
- Do not commit local TLS secrets, session key logs, or sensitive packet captures.
- Do not disable certificate verification in production.
- Production deployments require appropriate certificate trust, private-key protection, and certificate renewal.

### Learning outcomes

Through this project, we practiced:

- HTTPS and TLS fundamentals.
- Certificate purpose and validation.
- TLS 1.3 key establishment and traffic-key derivation.
- HTTPS configuration in Uvicorn.
- Request processing through FastAPI.
- Testing and inspecting TLS using Postman, OpenSSL, curl, and Wireshark.
- Understanding the difference between encrypted communication and trusted server identity.

---

## ⭐ Final Takeaway

> HTTPS uses TLS to protect HTTP communication in transit. The TLS handshake establishes the security context, Uvicorn handles TLS in this project, and FastAPI processes the application request and generates the response.