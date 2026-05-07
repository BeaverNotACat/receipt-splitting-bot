<p align="center">
  <a href="https://github.com/BeaverNotACat/receipt-splitting-bot" target="_blank" rel="noopener noreferrer">
    <img width="300" height="300" alt="receipt-svgrepo-com" src="https://github.com/user-attachments/assets/c3e97afb-0db7-4d45-a68c-9a832269cfc5" />
  </a>
</p>
<h1 align="center">Receipt Splitting Bot</h1>
<p align="center">
    <strong>Intelligent collective spending management tool</strong>
</p>

---
Badges go here

---

## 📝 Table of Contents
> **Quick Navigation** - Jump to any section below

- [📖 Overview](#-overview)
  - [✨ Features](#-features)
- [📚 Documentation](#-documentation)
  - [🚀 Self-host Guide](#-self-host-guide)
  - [💻 Developers guide](#-developers-guide)
- [🙏 Special Thanks](#-special-thanks)

---
# 📖 Overview
> **What is the Receipt Splitting Bot?**

The Receipt Splitting Bot is a tool for managing collective spending using natural language on the surface, and serves as a good example of an agent-based application under the hood.  
It is built with a Python infrastructure and LangChain. It combines extensibility and modularity under the hood with the robustness of strict linting and thoughtfull testing.

If you speak russian [**try us here**](https://t.me/ReceiptSplittingBot)

## ✨ Features:
- Integrated LLM for logic orchestration and natural language control
- CV and ASR technologies for understanding photos and voice messages
- Collaborative spending management

# 📚 Documentation
## 🚀 Self-host Guide
We provide a Docker image at GHCR: `ghcr.io/beavernotacat/receipt-splitting-bot:latest`  
For more information, you can check our releases.

For proper operation, the application requires a Redis-compatible key-value store and a PostgreSQL database. A sample Compose file looks can be found in repo as `production.compose.yaml`

**All environment variables are listed in the `.env.example` file**

## 💻 Developers guide

If you want to contribute to this project, please read our [contribution guidelines](https://github.com/BeaverNotACat/receipt-splitting-bot?tab=contributing-ov-file).

We also have articles in the `docs/` directory describing the project vision and explaining design decisions.

# 🙏 Special Thanks
[TBank](khttps://www.tbank.ru/)
— for the R&D hackathon where the project was born
 
[Matv864](https://github.com/matv864)
— for contributing
