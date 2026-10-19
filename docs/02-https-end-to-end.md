# 02. HTTPS — End-to-End Explanation

## 1. What Is HTTPS?

HTTPS stands for Hypertext Transfer Protocol Secure. It is HTTP communication protected by TLS (Transport Layer Security).

HTTP defines how a client sends requests and receives responses. TLS protects that communication while it travels across the network.

For example, when Postman requests `https://localhost:8000/`, HTTPS protects the HTTP request and response using TLS.

**Simple idea:** HTTP defines the communication; TLS secures it.

## 2. Why Do We Need HTTPS?

Without encryption, an observer who can capture ordinary HTTP traffic may be able to read its contents.

HTTPS addresses three important security requirements:

- **Confidentiality:** Prevents network observers from reading protected application data.
- **Integrity:** Detects unauthorized modification of protected data.
- **Authentication:** Helps the client verify that it is communicating with the intended server.

HTTPS does not automatically make an application secure against every attack. Application vulnerabilities, stolen credentials, and compromised devices still require separate protection.

## 3. The Main Components of HTTPS

HTTPS involves several components working together:

| Component | Purpose |
|---|---|
| Client | Initiates the connection; in our project, Postman or curl |
| TCP | Provides the underlying connection for TLS over TCP |
| TLS | Negotiates security and protects application data |
| Server certificate | Provides the server's identity information and public key |
| Private key | Secret key used by the server for cryptographic operations |
| Traffic keys | Symmetric keys used to protect TLS records |
| HTTP | Defines the application request and response |
| FastAPI | Handles the request and produces the application response |

These components have different responsibilities. HTTP does not perform the TLS handshake, and FastAPI does not directly encrypt each response in our current setup.

## 4. Step 1 — Establish the TCP Connection

Before TLS can operate over TCP, the client establishes a TCP connection with the server.

In our project, the server listens on:

`127.0.0.1:8000`

The client connects to that address and port. TCP establishes the connection through its handshake, commonly described as SYN, SYN-ACK, and ACK.

Once TCP is established, the client and server can exchange TLS handshake messages.

**Important:** TCP establishes the transport connection; it does not itself encrypt HTTP data.

## 5. Step 2 — Perform the TLS Handshake

After the TCP connection is established, the client and server perform a TLS handshake.

In TLS 1.3, the main steps include:

1. **ClientHello:** The client offers supported TLS versions, cryptographic options, and key-exchange information.
2. **ServerHello:** The server selects compatible parameters and provides its key-exchange information.
3. **Server authentication:** The server normally sends its certificate and proves possession of the corresponding private key.
4. **Key establishment:** Both sides derive shared secrets and the traffic keys needed for protected communication.
5. **Finished messages:** The handshake is cryptographically confirmed.

Most TLS 1.3 handshake messages after ServerHello are encrypted. The exact handshake can vary depending on the connection and negotiated options.

The detailed sequence is explained in `03-tls-handshake.md`.

## 6. Step 3 — Understand the Certificate and Trust

The server certificate provides information about the server's identity and contains its public key.

The client checks whether the certificate is valid for the requested hostname, within its validity period, and trusted under its certificate-validation rules.

Our project uses a **self-signed certificate** for `localhost`. This certificate is not automatically trusted by every client.

A TLS connection may still negotiate encryption when a client skips certificate verification, but that does not establish that the server's identity has been trusted.

**Remember:** Encryption and certificate trust are related, but they are not the same thing.

## 7. Step 4 — Establish Traffic Keys

TLS 1.3 commonly uses ephemeral Diffie–Hellman key exchange, such as X25519, to establish shared secret material.

The client and server exchange public key-share information. Each side uses its own private ephemeral value and the other side's public share to derive the same shared secret.

That secret is not sent directly across the network.

TLS then uses a key-derivation process based on HKDF to derive handshake and application traffic secrets, from which the appropriate symmetric encryption keys and initialization values are derived.

These traffic keys protect application data in both directions.

## 8. Step 5 — Send and Process the HTTPS Request

Once the TLS connection is ready, the client sends its HTTP request through TLS.

For our project, the request might be:

`GET / HTTP/1.1`

Conceptually, the flow is:

1. Postman creates the HTTP request.
2. TLS protects the request in encrypted TLS records.
3. The records travel through the established TCP connection.
4. Uvicorn's TLS layer receives and decrypts the records.
5. Uvicorn passes the resulting HTTP request to FastAPI.
6. FastAPI executes the matching endpoint.

The network carries TLS-protected data, while FastAPI receives the decrypted HTTP request.

## 9. Step 6 — Return the Encrypted Response

Our FastAPI `/` endpoint returns JSON similar to:

```json
{
  "message": "HTTPS is working!",
  "project": "HTTPS-PROJECT",
  "status": "secure connection"
}
```

The response flow is:

1. FastAPI generates the JSON response.
2. Uvicorn's TLS layer protects the HTTP response using the server-to-client traffic keys.
3. The encrypted TLS records travel through TCP.
4. The client decrypts the records and reconstructs the HTTP response.
5. Postman displays the status, headers, and JSON body.

The response uses the established TLS connection; the handshake is not normally repeated for every HTTP request on that connection.

## 10. Complete HTTPS Flow

The overall sequence is:

```text
Client (Postman)
       |
       | 1. Establish TCP connection
       v
TCP Connection
       |
       | 2. TLS handshake
       v
TLS Secure Connection
       |
       | 3. Encrypted HTTP request
       v
Uvicorn TLS Layer
       |
       | 4. Decrypt request
       v
FastAPI Application
       |
       | 5. Process endpoint and create JSON
       v
Uvicorn TLS Layer
       |
       | 6. Encrypt HTTP response
       v
TLS / TCP
       |
       | 7. Protected response
       v
Client (Postman)
```

### Key Takeaways

- TCP establishes the connection; TLS establishes security over it.
- The certificate supports server authentication, while traffic keys protect application data.
- The client and server derive shared secrets; the shared secret is not sent directly.
- Uvicorn handles TLS in our setup, while FastAPI handles application logic.
- HTTPS protects data in transit, but certificate validation and application security still matter.