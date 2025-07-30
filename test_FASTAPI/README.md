# 📁 ProviCloud File Handling Service

This FastAPI-based application provides file download functionality from S3 buckets, with secure configuration via environment-based secrets and optional encrypted URL tokens for secure access.

---

## 🚀 Features

- ⚡ Built with FastAPI
- 🔒 Secrets loaded securely from files based on the environment
- ☁️ Supports S3 file download via `boto3`
- 📡 `/s3/health` endpoint to verify S3 connectivity
- 🔐 Optional: Encrypted token support for secure file downloads

---

## 📁 Project Structure

```
backend/
├── custom_uvicorn.py            # Entry point to launch FastAPI
├── src/
│   ├── main.py                  # FastAPI app creation & router setup
│   ├── core/
│   │   └── config.py            # Settings & secret loading
│   ├── routers/
│   │   └── file_handling_router.py
│   ├── modules/
│   │   └── file_handling/
│   │       └── file_handling_service.py
│   ├── helpers/
│   │   └── logger.py, common.py
│   └── db/
│       └── session.py, base_class.py
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd backend
```

### 2. Create Secrets Directory

#### ✅ Local Development

Create the following directory and add secret files:

```
C:/Users/IBISWAS/Desktop/MBRDI-Projects/secrets/
```

#### 🖋️ Files to include (one value per file):

```
ENV=local (optional - can also be passed as ENV var)
DBUSER
DBPWD
DBHOST
PORT
DBNAME
X_API_KEY
AWS_ACCESS
AWS_SECRET
BUCKET_NAME
ENDPOINT_URL
```

#### ✅ Production Environment

Place secret files under:

```
/etc/secrets/
```

---

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

> Required packages: `fastapi`, `uvicorn`, `boto3`, `sqlalchemy`, `aiofiles`, `cryptography`, `python-multipart`, etc.

---

### 4. Run the Application

```bash
python custom_uvicorn.py
```

---

## 📡 API Endpoints

### ✅ S3 Health Check

```
GET /s3/health
```

Returns list of accessible buckets.

**Response:**
```json
{
  "status": "success",
  "buckets": ["your-bucket-name"]
}
```

---

### 📥 Download File from S3

```
GET /download/{filename}
```

Downloads a file by filename from the configured S3 bucket.

---

## 🔐 Optional: Encrypted Download URL

Instead of sending the filename directly, you can encrypt it using `cryptography.Fernet`:

### 🔧 Encrypt Parameters

```python
from cryptography.fernet import Fernet

key = Fernet.generate_key()
fernet = Fernet(key)

def encrypt(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
```

Then access via:

```
GET /download?token=<encrypted-token>
```

> Example payload: `{ "filename": "example.csv", "expires_at": "2025-06-12T12:00:00Z" }`

---

## 🧪 Testing with Postman or curl

```bash
curl http://127.0.0.1:8000/s3/health
curl http://127.0.0.1:8000/download/sample.csv
```

---

## 🌐 Environment Control

| Key         | Description                                |
|--------------|--------------------------------------------|
| ENV         | `local` or `production` for secrets path   |
| DBUSER      | Database user                              |
| AWS_*       | S3 access credentials                      |
| BUCKET_NAME | Target S3 bucket                           |
| ENDPOINT_URL| S3 endpoint (MinIO or AWS)                 |

---

## 📌 Best Practices

- Use HTTPS in production to encrypt the full URL in transit.
- Use encrypted tokens to protect sensitive parameters.
- Never hardcode secrets; use secret files or env vars.

---

## 📞 Support

For issues, please open a ticket or contact the backend team.

---