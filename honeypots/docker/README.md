# Basic Honeypots

Dockerized honeypot deployment for security monitoring and attack data collection.

## Honeypots

| Honeypot       | Type          | Port   |
| -------------- | ------------- | ------ |
| Cowrie         | SSH Honeypot  | 22/tcp |
| Dionaea        | FTP Honeypot  | 21/tcp |
| Tanner + Snare | HTTP Honeypot | 80/tcp |

---

## Requirements

* Docker
* Docker Compose

Check installation:

```bash
docker --version
docker compose version
```

---

# Run All Honeypots

From this directory (`docker/`):

```bash
docker compose up -d
```

Check running containers:

```bash
docker ps
```

Expected containers:

```
cowrie
dionaea
tanner
tanner_api
tanner_redis
tanner_phpox
snare
```

---

# Run Individual Honeypots

## Cowrie

```bash
cd cowrie
docker compose up -d
```

Port:

```
22/tcp
```

---

## Dionaea

```bash
cd dionaea
docker compose up -d
```

Port:

```
21/tcp
```

---

## Tanner + Snare

```bash
cd tanner
docker compose up -d
```

Port:

```
80/tcp
```

---

# Stop Honeypots

Stop all honeypots:

```bash
docker compose down
```

Stop a specific honeypot:

Example:

```bash
cd cowrie
docker compose down
```

---

# Logs

## Cowrie

```bash
cat ../data/cowrie/log/cowrie.json
```

## Dionaea

```bash
cat ../data/dionaea/log/dionaea.json
```

## Tanner

```bash
cat ../data/tanner/log/tanner_report.json
```

---

# Project Structure

```
docker/

├── README.md
├── docker-compose.yml
│
├── cowrie/
│   └── docker-compose.yml
│
├── dionaea/
│   └── docker-compose.yml
│
└── tanner/
    └── docker-compose.yml
```

Data:

```
data/

├── cowrie/
├── dionaea/
└── tanner/
```
# Test Honeypots

After starting all honeypots, you can test each service and check the generated logs.

---

## Test Cowrie (SSH Honeypot)

Connect:

```bash
ssh root@localhost -p 22
```

Try some commands:

```bash
ls
pwd
whoami
uname -a
cat /etc/passwd
```

View logs:

```bash
cat cowrie/data/log/cowrie.json
```

---

## Test Dionaea (FTP Honeypot)

Connect:

```bash
ftp localhost
```

Try login:

```
Username: admin
Password: admin
```

View logs:

```bash
cat dionaea/data/log/dionaea.json
```

---

## Test Tanner + Snare (HTTP Honeypot)

Open browser:

```
http://localhost
```

or test using curl:

```bash
curl -i http://localhost
```

View logs:

```bash
cat tanner/data/tanner_report.json
```

---
