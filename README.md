# Enigma Machine Simulation 🔐
A Python implementation of the **Enigma Machine**, the famous cipher device used during World War II.

## ✨ Features
- Plugboard simulation (letter swaps before and after the rotors)  
- Configurable rotors (I, II, III, IV, V) with correct wiring and notch positions  
- Reflector options (B, C) with fixed mappings  
- Accurate rotor stepping including **double-stepping**  
- Encryption and decryption using the same machine settings  
- Colored console output using `colorama`  

## 📂 Files

enigma_machine.py # Main Python file
README.md # Documentation

## ⚙️ Installation
Make sure you have Python **3.7+** installed.  
Install dependencies with:
```bash
pip install colorama

▶️ Usage

Run the script:

python enigma_machine.py

Example Output
Welcome To Enigma Machine
Plaintext : SHAKILA MALIK
Ciphertext: XYQJTNX RXNUN
Decrypted : SHAKILA MALIK

🛠️ Configuration

You can customize the machine by choosing:

Rotor order (I, II, III, IV, V)

Reflector (B or C)

Plugboard pairs (e.g., ["AV","BS","CG"])

Ring settings (default: (0,0,0))

Starting positions (e.g., "AAA")

Example:

enigma = build_example_enigma(
    left='I',
    middle='II',
    right='III',
    reflector='B',
    plug_pairs=["AV","BS","CG"],
    start_positions="MCK"
)

📖 Historical Note

The Enigma Machine was used by Nazi Germany for secure communication during WWII. Its encryption was eventually broken by Allied cryptanalysts, including Alan Turing, which played a vital role in ending the war.

📝 License

This project is for educational purposes only. You are free to use and modify it.


Do you also want me to make a **GitHub-ready description** (short version) that you can paste in the repo “About” section?
