# API Documentation

## Authorization

All API requests require the use of a generated API key. You can find your API key, or generate a new one, by sending request to `POST /api/auth/login` endpoint.

To authenticate an API request, you should provide your API key in the `Authorization` header. Please bare in mind, we are using `Bearer Token`.

```http
POST /api/auth/login
```

| Parameter | Type | Location | Description |
| :--- | :--- | :--- | :--- |
| `username` | `string` | `JSON Body` | **Required**. Your Username |
| `password` | `string` | `JSON Body` | **Required**. Your Password |

## Accessible APIs
- Login status
```http
GET /api/auth/login
```

| Parameter | Type | Location | Description |
| :--- | :--- | :--- | :--- |
| `access_token` | `string` | `Authorization` | **Required**. Your Access Token; `Bearer <token>` |

