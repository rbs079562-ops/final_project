# Demystifying Ransomware: A Technical Study

## 🛡️ Project Overview
This project is a functional simulation of a ransomware attack lifecycle, developed as a final project for a Cybersecurity Major. It explores infection, exfiltration, and cryptographic recovery.

## 📁 Components
* **Encryptor GUI:** Simulates the payload execution and file locking.
* **C2 Server:** A Python-based Command & Control listener for key harvesting.
* **Recovery Tool:** A decryptor utility requiring the secret key.
* **Defender Tool:** An analysis script that recovers files WITHOUT the key via XOR cryptanalysis.

## ⚠️ ETHICAL WARNING
This code is for **educational purposes only**. It is designed to run in a controlled Virtual Machine environment. Targeting systems without permission is illegal.

## 🚀 How to Run
1. Create a folder `Ransomware_Test_Folder` on your Desktop.
2. Run `malware_server.py`.
3. Run `encryptor_gui.py` to simulate the attack.
4. Use `defender.py` to demonstrate keyless recovery.
