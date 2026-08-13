import asyncio
from datetime import datetime, timezone
from random import choice, randint
from app.models.schemas import AttackEvent


HONEYPOTS = [
    {
        "name": "Cowrie",
        "protocol": "SSH",
        "attack_types": ["Brute Force", "Credential Attack", "Command Injection"],
    },
    {
        "name": "Dionaea",
        "protocol": "TCP",
        "attack_types": ["Malware", "Port Scan", "Exploit Attempt"],
    },
    {
        "name": "Tanner",
        "protocol": "HTTP",
        "attack_types": ["Web Attack", "SQL Injection", "Command Injection"],
    },
]

SOURCE_IPS = [
    "185.12.34.56",
    "45.77.21.10",
    "91.203.44.18",
    "103.25.67.90",
]

COUNTRIES = [
    ("Egypt", "EG"),
    ("Germany", "DE"),
    ("United States", "US"),
    ("France", "FR"),
]

SEVERITIES = ["Low", "Medium", "High", "Critical"]


def generate_mock_event():

    honeypot = choice(HONEYPOTS)
    country, country_code = choice(COUNTRIES)

    event = AttackEvent(
        timestamp=datetime.now(timezone.utc)
        honeypot=honeypot["name"],
        protocol=honeypot["protocol"],
        source_ip=choice(SOURCE_IPS),
        source_port=randint(1024, 65535),
        destination_ip="192.168.1.100",
        destination_port=22 if honeypot["name"] == "Cowrie" else 80,
        session_id=f"session-{randint(1000, 9999)}",

        username="admin" if honeypot["name"] == "Cowrie" else None,
        password="123456" if honeypot["name"] == "Cowrie" else None,

        user_attempt=randint(1, 10),
        pass_attempt=randint(1, 10),
        auth_attempt=randint(1, 10),
        command_count=randint(0, 20),

        country=country,
        country_code=country_code,
        asn=randint(1000, 99999),

        attack_type=choice(honeypot["attack_types"]),
        severity=choice(SEVERITIES),

        source_dataset="mock"
    )

    return event


async def mock_event_producer(manager):

    while True:

        event = generate_mock_event()

        await manager.broadcast(
            event.model_dump(mode="json")
        )

        await asyncio.sleep(5)