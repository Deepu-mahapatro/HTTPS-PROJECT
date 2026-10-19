# 01. HTTPS Project Overview

## 1. Project Introduction

This project demonstrates how HTTPS secures communication between a client and a web server using TLS (Transport Layer Security).

We implemented a FastAPI application and configured Uvicorn to serve it over HTTPS using a locally generated self-signed certificate and its corresponding private key.

The project focuses on understanding how HTTPS works internally, from establishing a secure connection to sending an HTTP request and receiving an encrypted response.

## 2. Project Objectives

The main objectives are:

- Understand the difference between HTTP and HTTPS.
- Learn the purpose of TLS and the TLS handshake.
- Understand server certificates and private keys.
- Learn how clients and servers establish shared traffic keys.
- Observe TLS handshake packets using Wireshark.
- Test HTTPS endpoints using Postman, curl, and OpenSSL.
- Understand how Uvicorn and FastAPI work together.

## 3. What Is HTTPS?

HTTPS stands for Hypertext Transfer Protocol Secure. It is HTTP communication protected by TLS.

HTTP defines how clients and servers exchange requests and responses. TLS provides security for that communication.

HTTPS primarily provides:

- **Confidentiality:** Protects application data from being read by network observers.
- **Integrity:** Helps detect unauthorized modification of transmitted data.
- **Authentication:** Allows the client to verify the server's identity when certificate validation succeeds.

## 4. Technologies Used

The project uses the following tools:

| Technology | Purpose |
|---|---|
| Python | Programming language |
| FastAPI | Defines API endpoints and application logic |
| Uvicorn | Runs the application and handles HTTPS/TLS |
| OpenSSL | Generates and inspects the local certificate and private key |
| Postman | Sends HTTPS requests and displays responses |
| curl | Tests HTTPS endpoints from the terminal |
| Wireshark | Captures and inspects network packets |
| VS Code | Development environment |
| Git and GitHub | Version control and project hosting |

## 5. Project Features

- A FastAPI application with `/` and `/health` endpoints.
- Local HTTPS configuration using Uvicorn.
- A self-signed TLS certificate for development and testing.
- HTTPS request testing using Postman and curl.
- TLS connection inspection using OpenSSL.
- Packet capture and handshake inspection using Wireshark.
- Documentation of the HTTPS handshake and complete request-response flow.

## 6. Certificate and Private Key

The project uses two local files:

- `certs/server.crt` — the server certificate containing identity information and the server's public key.
- `certs/server.key` — the corresponding private key, which must remain secret.

The certificate was generated locally and is self-signed. Therefore, clients do not automatically trust it as they would a certificate issued by a trusted certificate authority.

The certificate and private key are used by Uvicorn to configure HTTPS. They are not generated separately for every HTTP request.

**Security note:** These local files are excluded from GitHub. The private key must never be committed or shared.

## 7. How the Project Works

The client first connects to the server and establishes a TCP connection. The TLS handshake then negotiates security parameters, authenticates the server when verification succeeds, and establishes traffic keys.

After TLS is established:

1. Postman sends an HTTPS request.
2. TLS encrypts the HTTP request for transmission.
3. Uvicorn's TLS layer decrypts the request.
4. FastAPI processes the request and generates a response.
5. Uvicorn's TLS layer encrypts the HTTP response.
6. Postman receives and displays the response.

This separates transport security from application logic.

## 8. Testing and Verification

We used several tools to investigate different parts of the system:

- **Postman:** Sent HTTPS requests to the FastAPI endpoints.
- **curl:** Confirmed that the endpoints returned the expected JSON.
- **OpenSSL:** Inspected the negotiated TLS protocol, cipher suite, and certificate verification result.
- **Wireshark:** Observed TCP traffic, ClientHello, ServerHello, and TLS application-data records.

The local HTTPS endpoint returned the expected application response. OpenSSL also reported TLS 1.3 during our connection test.

Because the certificate is self-signed, certificate trust must be handled separately from establishing an encrypted TLS connection.

## 9. Project Scope and Limitations

This is a local learning project, not a production deployment.

The self-signed certificate is intended for development and does not provide automatic public trust. Testing with `curl -k` disables certificate verification and must not be treated as proof that the certificate is trusted.

The project demonstrates HTTPS fundamentals but does not implement a complete production security architecture, public certificate management, or a production reverse proxy.

## 10. Learning Outcomes

After completing this project, we can explain:

- How HTTPS uses TLS to protect HTTP communication.
- Why a server certificate and private key are needed.
- How a TLS handshake establishes secure communication.
- How traffic keys protect application data.
- How Uvicorn and FastAPI process an HTTPS request.
- How Postman, OpenSSL, curl, and Wireshark help test and inspect HTTPS.
- Why encrypted communication and certificate trust are related but different concepts.

The project provides a practical foundation for understanding HTTPS before studying production TLS configuration and deployment.