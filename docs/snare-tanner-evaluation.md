```markdown
# SNARE & Tanner Honeypot Evaluation

## Overview

As part of the Smart Honeypot Orchestrator & Threat Intelligence Dashboard project, SNARE and Tanner were evaluated as HTTP honeypot solutions to understand their deployment process, interaction capabilities, logging behavior, and their suitability for capturing attacker activities.

The goal of this evaluation was not only to deploy a fake web service, but also to analyze what type of information can be collected from attacker interactions and how these logs can be used later in the project.

---

## SNARE Overview

SNARE is a web application honeypot that creates a fake website by cloning or using predefined web pages. It listens for incoming HTTP requests and records visitor interactions.

During testing, a fake banking login page was deployed. The page contained a login form that allowed us to simulate attacker behavior such as:

- Visiting the website.
- Accessing specific URLs.
- Submitting login credentials.
- Sending HTTP requests.

SNARE successfully captured these interactions and stored them in its log files.

---

## Deployment

SNARE was deployed using Docker.

The running architecture:

```

User / Attacker
|
|
v
SNARE Honeypot
|
|
v
Tanner
|
|
v
Logs / Analysis

```

SNARE was exposed on:

```

HTTP Port: 80

```

Tanner was running as the analysis backend:

```

Tanner API:
8090

Tanner Web:
8091

```

---

## Testing Scenario

A fake banking login page was deployed.

The testing flow:

1. Access the honeypot website.
2. Navigate to the login page.
3. Enter fake credentials.
4. Submit the login form.
5. Analyze generated logs.

Example:

```

Username:
admin

Password:
123456

```

---

## SNARE Logs

SNARE stores HTTP interaction logs inside:

```

/opt/snare/snare.log

```

The logs include useful information such as:

- Requested URL paths.
- HTTP methods.
- Source IP addresses.
- User-Agent information.
- Submitted POST parameters.

Example captured event:

```

Request path: /doLogin

POST data:

uid: admin
passw: 123456
btnSubmit: Login

```

This shows that SNARE was able to capture the credentials entered into the fake login form.

---

## Tanner Overview

Tanner works as the analysis engine behind SNARE.

While SNARE is responsible for receiving HTTP traffic and serving the fake website, Tanner analyzes the collected requests and generates structured reports.

Tanner provides:

- Request analysis.
- Detection modules.
- Session tracking.
- Structured JSON reports.

The generated report file:

```

/tmp/tanner/tanner_report.json

````

contains details about HTTP activity.

Example fields:

```json
{
"method":"GET",
"path":"/",
"status":200,
"peer":{
    "ip":"172.19.0.1"
}
}
````

---

## Interaction Level

SNARE and Tanner are considered low-interaction web honeypots.

They do not provide a real vulnerable operating system or a complete backend application.

Instead, they simulate web applications and collect attacker behavior at the HTTP level.

The captured behavior includes:

* URL enumeration.
* Login attempts.
* Credential submission.
* HTTP request patterns.
* User-Agent information.
* Session activity.

However, they do not provide:

* Real command execution.
* Shell access.
* Malware execution environment.
* Full attacker post-exploitation behavior.

---

## Observed Limitations

During testing, several limitations were observed:

### 1. Limited Web Interaction

The fake website works mainly as a trap for collecting requests. It does not behave like a real banking application.

For example, after submitting credentials, the main goal is logging the attempt rather than providing a complete authentication workflow.

---

### 2. Static Website Dependency

SNARE requires a prepared website structure.

The honeypot depends on the captured page files and metadata.

A realistic website requires:

* HTML files.
* Images.
* CSS files.
* JavaScript files.
* Correct page mappings.

Missing files may generate 404 responses.

---

### 3. Limited Behavior Visibility

SNARE/Tanner can capture web-based behavior, but they cannot observe deeper attacker actions after gaining access because there is no real system behind the application.

---

## Final Evaluation

SNARE and Tanner were successfully deployed and tested as HTTP honeypot components.

The evaluation showed that:

* SNARE can simulate realistic web pages.
* User interactions and submitted data can be captured.
* Tanner provides structured analysis of HTTP requests.
* The collected logs can be integrated into a larger monitoring pipeline.

For the Smart Honeypot Orchestrator project, SNARE/Tanner can be used as the HTTP deception layer, while other honeypots such as Cowrie and Dionaea can provide deeper visibility for SSH attacks and malware-related activities.

```
```
