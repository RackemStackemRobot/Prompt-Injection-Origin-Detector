# Disclaimer

This project is provided as-is for research, educational, and experimental use.

It is not a security product, a compliance solution, or a guarantee of protection against prompt injection, data exfiltration, or other attacks. The tools in this repository are intended to support observability, debugging, and forensic analysis of AI agent pipelines, not to replace proper security architecture, access controls, or governance mechanisms.

## No guarantee of detection

Detection in this project is heuristic and pattern-based.  
It may produce false positives, false negatives, or miss obfuscated attacks entirely.

Accurate origin attribution depends on the completeness and correctness of runtime trace logs.  
If intermediate steps are not logged, the tool cannot infer where malicious instructions originated.

## Not legal or security advice

Nothing in this repository should be interpreted as legal advice, security advice, or compliance guidance.  
You are responsible for evaluating these tools in the context of your own systems, threat models, and regulatory requirements.

## Data sensitivity

Trace logs and previews may contain sensitive or confidential information.

You are responsible for:

- redacting secrets and tokens before logging  
- securing trace files  
- complying with applicable privacy and data handling laws  
- avoiding logging personal or regulated data without appropriate controls  

## Use at your own risk

You assume all risks associated with using this software.

The author makes no warranties, express or implied, regarding fitness for a particular purpose, security outcomes, or operational reliability.

## Responsible use

Do not use these tools for unauthorized monitoring, surveillance, or data collection.  
Only analyze logs and systems you own or have explicit permission to test.
