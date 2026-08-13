MOCK_STATISTICS = {
    "totalAttacks": 1284,
    "uniqueSources": 327,
    "countries": 42
}


MOCK_RECENT_EVENTS = [
    {
        "id": 1,
        "honeypot": "Cowrie",
        "sourceIp": "192.168.1.10",
        "country": "Egypt",
        "attackType": "SSH Brute Force",
        "timestamp": "2026-08-10T12:30:00"
    },
    {
        "id": 2,
        "honeypot": "Dionaea",
        "sourceIp": "10.0.0.25",
        "country": "United States",
        "attackType": "Malware",
        "timestamp": "2026-08-10T12:25:00"
    },
    {
        "id": 3,
        "honeypot": "Tanner",
        "sourceIp": "172.16.0.15",
        "country": "Germany",
        "attackType": "Web Attack",
        "timestamp": "2026-08-10T12:20:00"
    }
]


MOCK_TOP_ATTACKERS = [
    {
        "ip": "192.168.1.10",
        "attacks": 245
    },
    {
        "ip": "10.0.0.25",
        "attacks": 187
    },
    {
        "ip": "172.16.0.15",
        "attacks": 132
    }
]

MOCK_COUNTRIES = [
    {
        "country": "Egypt",
        "attacks": 320
    },
    {
        "country": "United States",
        "attacks": 275
    },
    {
        "country": "Germany",
        "attacks": 198
    },
    {
        "country": "Russia",
        "attacks": 156
    },
    {
        "country": "China",
        "attacks": 143
    }
]

MOCK_ATTACK_EVENT = {
    "timestamp": "2026-08-11T21:11:20.701152",
    "honeypot": "Cowrie",
    "protocol": "SSH",
    "source_ip": "185.12.34.56",
    "source_port": None,
    "destination_ip": None,
    "destination_port": None,
    "session_id": "test-session-001",
    "username": None,
    "password": None,
    "user_attempt": 0,
    "pass_attempt": 0,
    "auth_attempt": 0,
    "anonymous": 0,
    "command_count": 0,
    "country": None,
    "country_code": None,
    "asn": None,
    "ip_reputation": None,
    "attack_type": "Brute Force",
    "mitre_technique": None,
    "attack_stage": None,
    "severity": "High",
    "source_dataset": "mock"
}