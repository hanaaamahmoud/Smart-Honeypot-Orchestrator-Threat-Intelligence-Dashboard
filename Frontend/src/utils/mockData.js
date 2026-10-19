export const mockStatistics = {
  totalAttacks: 1284,
  activeHoneypots: 3,
  uniqueSources: 327,
  countries: 42,
};

export const mockAttackTrend = [
  { time: "10:00", attacks: 12 },
  { time: "11:00", attacks: 18 },
  { time: "12:00", attacks: 15 },
  { time: "13:00", attacks: 27 },
  { time: "14:00", attacks: 31 },
  { time: "15:00", attacks: 24 },
  { time: "16:00", attacks: 39 },
  { time: "17:00", attacks: 45 },
];

export const mockRecentAttacks = [
  {
    id: "evt-001",
    timestamp: "2026-08-06T10:30:00Z",
    sourceIp: "192.168.1.20",
    country: "Egypt",
    honeypot: "Cowrie",
    service: "SSH",
    eventType: "login_attempt",
    status: "failed",
  },
  {
    id: "evt-002",
    timestamp: "2026-08-06T10:42:00Z",
    sourceIp: "185.12.44.21",
    country: "Germany",
    honeypot: "Dionaea",
    service: "FTP",
    eventType: "authentication_attempt",
    status: "failed",
  },
  {
    id: "evt-003",
    timestamp: "2026-08-06T11:05:00Z",
    sourceIp: "45.88.12.7",
    country: "United States",
    honeypot: "Snare",
    service: "HTTP",
    eventType: "web_request",
    status: "detected",
  },
];

export const mockLiveAttacks = [
  {
    id: "live-001",
    timestamp: "10:42:31",
    sourceIp: "185.12.44.21",
    country: "Germany",
    honeypot: "Dionaea",
    service: "FTP",
    eventType: "Authentication Attempt",
    status: "failed",
  },
  {
    id: "live-002",
    timestamp: "10:43:08",
    sourceIp: "45.88.12.7",
    country: "United States",
    honeypot: "Snare",
    service: "HTTP",
    eventType: "Web Request",
    status: "detected",
  },
  {
    id: "live-003",
    timestamp: "10:44:17",
    sourceIp: "91.204.18.63",
    country: "Russia",
    honeypot: "Cowrie",
    service: "SSH",
    eventType: "Login Attempt",
    status: "failed",
  },
  {
    id: "live-004",
    timestamp: "10:45:02",
    sourceIp: "103.77.14.8",
    country: "India",
    honeypot: "Cowrie",
    service: "SSH",
    eventType: "Command Attempt",
    status: "detected",
  },
];

export const mockHoneypotStatus = [
  {
    id: "cowrie-01",
    name: "Cowrie",
    service: "SSH",
    status: "running",
    events: 128,
    lastActivity: "2 min ago",
  },
  {
    id: "snare-01",
    name: "Snare",
    service: "HTTP",
    status: "running",
    events: 74,
    lastActivity: "30 sec ago",
  },
  {
    id: "dionaea-01",
    name: "Dionaea",
    service: "FTP",
    status: "running",
    events: 42,
    lastActivity: "1 min ago",
  },
];
export const mockHoneypotDistribution = [
  {
    honeypot: "Cowrie",
    attacks: 612,
  },
  {
    honeypot: "Snare",
    attacks: 421,
  },
  {
    honeypot: "Dionaea",
    attacks: 251,
  },
];
