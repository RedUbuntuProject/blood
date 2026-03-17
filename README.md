BLOOD PACKAGE MANAGER 🩸
The Predator Package Manager for RedUbuntu & Cyber Security Tools

Blood is a high-performance, hybrid package manager designed for the RedUbuntu ecosystem. It prioritizes centralized shared libraries, minimizing system bloat while maintaining a fierce "Red Team" aesthetic.

⚡ FEATURES
Hybrid Hunting: Seamlessly switch between native .bld packages, Hypernova remote repositories, and silent OS fallback (APT).

Centralized Veins: All shared libraries are kept in /usr/lib/blood/ to prevent redundancy.

Predator Terminology: Uses aggressive, mission-oriented commands instead of standard IT jargon.

DNA Analysis: Built-in metadata validation via dna.json.

🛠️ INSTALLATION
To inject Blood into your system:

sudo cp blood.py /usr/local/bin/blood

sudo chmod +x /usr/local/bin/blood

🎮 USAGE
blood hunt [target] - Capture a package (Local, Remote, or OS)

blood eliminate [name] - Purge a package and its traces

blood scout [file] - Analyze a .bld file's DNA

blood forge [dir] - Forge a new .bld package

blood bleed - Purify system by shedding unused data

📦 THE .BLD FORMAT
Each .bld package must contain a dna.json file in its root with name, version, dependencies, and binary_path fields.

📜 LICENSE
Licensed under HD NPL v2.0 (Hypernova-Developer Nova Public License v2.0).
Proprietary developer tools and high-performance distribution rights reserved.

"Hunting is not just a command, it's a lifestyle." 🐉
