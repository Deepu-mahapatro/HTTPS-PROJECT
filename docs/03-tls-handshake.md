# 03. TLS 1.3 Handshake — End-to-End Explanation

## 1. What Is the TLS Handshake?

The TLS handshake is the process through which a client and server agree on security settings, authenticate the server, and establish cryptographic keys for protecting communication.

In our project, Postman initiates an HTTPS connection to the FastAPI application running through Uvicorn.

Before the HTTP request can be sent as protected application data, the client and server must establish the TLS connection.

**Purpose:** Agree on security parameters, verify server identity when certificate validation succeeds, and establish traffic keys.

## 2. Step 1 — ClientHello

The client starts the TLS handshake by sending a `ClientHello` message.

It can contain:

- Supported TLS versions.
- Supported cipher suites.
- A random value.
- Key-share information for ephemeral key exchange.
- Extensions such as Server Name Indication (SNI).

For our project, SNI can indicate the hostname `localhost`.

The key share provides public information that the server can use to establish shared secret material. The client does not send its private ephemeral key.

**Simple idea:** The client says, “Here are the security options I support, and here is my key-exchange information.”

## 3. Step 2 — ServerHello

The server responds with `ServerHello`.

It selects compatible security parameters, including the TLS version and cipher suite, and provides its key-share information for the agreed key-exchange group.

In our observed connection, the negotiated parameters included:

- **TLS version:** TLS 1.3.
- **Cipher suite:** `TLS_AES_256_GCM_SHA384`.
- **Key-exchange group:** X25519.

These parameters have different responsibilities. X25519 is used for ephemeral key exchange, AES-256-GCM protects TLS records, and SHA-384 is used by the TLS 1.3 key schedule.

**Simple idea:** The server says, “These are the security settings we will use, and here is my public key-exchange information.”

## 4. Step 3 — Derive the Shared Secret

In our connection, the client and server use ephemeral Diffie–Hellman key exchange with X25519.

Each side generates its own private ephemeral value and derives a corresponding public key share.

Conceptually:

1. The client sends its public key share.
2. The server sends its public key share.
3. The client combines its private ephemeral value with the server's public share.
4. The server combines its private ephemeral value with the client's public share.
5. Both sides derive the same shared secret material.

The shared secret itself is not transmitted over the network.

The two sides can calculate the same result because they use their own private value and the other side's public share.

**Important:** This shared secret is not yet the final application traffic key.

## 5. Step 4 — The Certificate and Server Authentication

The server normally sends a `Certificate` message containing its certificate chain.

A certificate contains information such as:

- Subject and issuer.
- Validity period.
- Subject public key.
- Subject Alternative Name (SAN).
- Digital signature and other certificate metadata.

The client checks the certificate according to its trust and validation rules. These checks can include the hostname, validity period, certificate chain, and trust anchor.

In TLS 1.3, the server also sends a `CertificateVerify` message when certificate-based authentication is used. This proves possession of the corresponding private key by signing handshake-related data.

Our project uses a self-signed certificate for `localhost`. It is not automatically trusted by all clients, so trust configuration matters.

**Important:** The certificate contains a public key, not the server's private key.

## 6. Step 5 — Derive the TLS Traffic Keys

After the key exchange provides shared secret material, TLS 1.3 uses a key-derivation process based on HKDF.

The process derives several secrets for different purposes:

1. Handshake traffic secrets protect encrypted handshake messages.
2. Application traffic secrets are used to derive keys for application-data protection.
3. Separate client-to-server and server-to-client traffic keys protect each direction.

The TLS 1.3 key schedule also incorporates handshake transcript information and other defined inputs.

For our negotiated cipher suite, AES-256-GCM protects TLS records. Each direction uses its own traffic keys and associated record-protection values.

**Simple idea:** The shared secret is an input to the key schedule; the traffic keys are derived from it, not sent directly across the network.

## 7. Step 6 — Encrypted Handshake Messages

After `ServerHello`, TLS 1.3 can protect subsequent handshake messages using handshake traffic keys.

For a typical certificate-authenticated full handshake, the server sends:

1. `EncryptedExtensions`
2. `Certificate`
3. `CertificateVerify`
4. `Finished`

These messages have different purposes:

- `EncryptedExtensions` carries negotiated extensions.
- `Certificate` supplies the certificate chain.
- `CertificateVerify` proves possession of the certificate's private key.
- `Finished` confirms the integrity of the handshake transcript using a cryptographic verification value.

Because most of these messages are encrypted in TLS 1.3, an ordinary Wireshark capture may not display their full contents without the appropriate session secrets.

The precise messages can vary depending on the handshake configuration.

## 8. Step 7 — Client Finished

After processing and validating the server's handshake messages, the client sends its own `Finished` message in a typical full handshake.

This message provides cryptographic confirmation of the handshake transcript.

The client and server must successfully verify the required handshake messages before considering the handshake complete.

Once the necessary handshake steps are finished, the client can send protected application data.

**Important:** `Finished` is not the user's HTTP request. It is part of the TLS handshake.

## 9. Step 8 — Encrypted Application Data

After the handshake, the client sends the HTTP request protected by the client-to-server application traffic keys.

For example:

`GET / HTTP/1.1`

The actual HTTP request is carried inside encrypted TLS records while traveling over the network.

The server's TLS layer decrypts the records and passes the HTTP request to FastAPI through Uvicorn.

FastAPI processes the route and produces a response. Uvicorn then protects the response with the server-to-client application traffic keys.

The client decrypts the response and displays the resulting JSON.

**The key distinction:** The HTTP data is protected by symmetric traffic keys; the certificate does not encrypt every request directly.

## 10. Complete TLS 1.3 Handshake Flow

```text
Client (Postman)                    Server (Uvicorn)
       |                                    |
       |---------- ClientHello ------------>|
       |   TLS options + client key share   |
       |                                    |
       |<--------- ServerHello -------------|
       |    Selected options + server share |
       |                                    |
       |  Both derive shared secret material|
       |  Both derive handshake traffic keys|
       |                                    |
       |<------ EncryptedExtensions --------|
       |<---------- Certificate ------------|
       |<------- CertificateVerify ---------|
       |<----------- Finished --------------|
       |                                    |
       | Validate certificate and handshake |
       |                                    |
       |------------ Finished ------------->|
       |                                    |
       |      TLS handshake completes       |
       |                                    |
       |==== Encrypted HTTP request =======>|
       |                                    |
       |<=== Encrypted HTTP response =======|
       |                                    |
```

This illustrates a typical full TLS 1.3 handshake using certificate-based server authentication and ephemeral key exchange. Exact message ordering and options can vary.

### Key Takeaways

- `ClientHello` and `ServerHello` establish the negotiated parameters and exchange key-share information.
- X25519 helps both sides derive shared secret material without sending that secret directly.
- The certificate and `CertificateVerify` support server authentication.
- HKDF derives handshake and application traffic secrets and the keys used to protect TLS records.
- `Finished` confirms handshake integrity.
- Once the handshake is complete, symmetric traffic keys protect the HTTP request and response.
