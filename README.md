<p align="center"><img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=38&duration=2800&pause=800&color=FF0000&center=true&vCenter=true&width=600&lines=NULLPHISH;Multi-Social+Phishing+Framework;Undetectable+%7C+12+Platforms;Your+Nightmare+Starts+Here" alt="NULLPHISH" /></p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20termux%20%7C%20macos-lightgrey?style=for-the-badge" />
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" />
  <img src="https://img.shields.io/github/stars/thisnull7/nullphish?style=social" />
  <img src="https://img.shields.io/github/forks/thisnull7/nullphish?style=social" />
</p>

# ═══ NULLPHISH ═══

**NULLPHISH** is a multi‑social media phishing framework built for educational security testing. It delivers pixel‑perfect replicas of login pages for **12 popular platforms**, captures credentials silently using anti‑detection techniques, and redirects victims to the real website without raising any browser alarm. The tool runs a local HTTP server, exposes it worldwide through Cloudflare Tunnel (or fallbacks), and logs every harvested account in structured JSON files.

> **⚠️ DISCLAIMER**  
> This software is provided for **educational purposes only**. Unauthorized use against individuals without their explicit consent is illegal. The developer assumes no liability for misuse. Always obtain proper permission before testing.

---

## 🎭 PREVIEW

<p align="center">
  <img src="https://raw.githubusercontent.com/thisnull7/nullphish/refs/heads/main/nullphish.png" alt="NULLPHISH Terminal Preview" width="600" />
</p>

---

## 🔥 FEATURES

- **12 realistic login pages** – Instagram, Facebook, Twitter/X, TikTok, Snapchat, Google, LinkedIn, GitHub, Microsoft, Yahoo, Netflix, Steam
- **Anti‑detection mechanism** – credentials are sent via JavaScript `fetch()`, avoiding browser phishing warnings
- **Instant redirect** – after capture, the victim is seamlessly forwarded to the genuine site
- **Multi‑tunnel** – Cloudflare Tunnel (auto‑download, no account), Serveo SSH, and localhost.run as fallbacks
- **Cross‑platform** – works on Windows, Kali Linux, macOS, and Termux (Android)
- **Auto port handling** – detects and kills conflicting processes, or switches to a free port
- **Structured logging** – each set of credentials saved to `creds_<platform>.json` with IP, user‑agent and timestamp
- **Intimidating terminal UI** – red ASCII art, color‑coded output, spinners, and real‑time capture alerts

---

## 📦 SUPPORTED PLATFORMS

| # | Platform | Port |
|---|----------|------|
| 1 | Instagram | 8080 |
| 2 | Facebook | 8081 |
| 3 | Twitter / X | 8082 |
| 4 | TikTok | 8083 |
| 5 | Snapchat | 8084 |
| 6 | Google | 8085 |
| 7 | LinkedIn | 8086 |
| 8 | GitHub | 8087 |
| 9 | Microsoft | 8088 |
|10 | Yahoo | 8089 |
|11 | Netflix | 8090 |
|12 | Steam | 8091 |

Each platform gets its own port so you can run multiple instances simultaneously.

---

## ⚙️ INSTALLATION

```bash
git clone https://github.com/thisnull7/nullphish.git
cd nullphish
pip install -r requirements.txt