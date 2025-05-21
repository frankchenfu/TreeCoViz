# 🌳 TreeCoViz: Phylogenetic Tree Comparison and Visualization Tool

**TreeCoViz** is a lightweight, user-friendly graphical software designed for **visualizing and comparing phylogenetic trees**. It supports Newick format input, customizable comparison and visualization parameters, and interactive outputs, making it suitable for researchers and students in computational biology and bioinformatics.

---

## 🖼 Sample Screenshot

> <img width="918" alt="screenshot" src="https://github.com/user-attachments/assets/acfa77a1-1b92-45d7-8ca7-135987fc2b34" />

> Example comparing two Newick-format trees and displaying their Largest Common Subtree.

---

## 📥 Installation Instructions

### 🪟 Windows 10/11 (64-bit)

* Download the precompiled executable: **`TreeCoViz.exe`**
* Simply **double-click** to launch the application. No installation or setup required.

📌 [See the latest release](https://github.com/frankchenfu/TreeCoViz/releases)

---

### 🐧 Ubuntu 20.04 / 22.04 (including WSL)

* Download the executable: **`TreeCoViz`**
* Open a terminal, navigate to the downloaded directory, and run:

```bash
chmod +x TreeCoViz
./TreeCoViz
```

#### ✅ Required Dependencies (first-time setup only)

To ensure proper display of the graphical interface (via Qt), run:

```bash
sudo apt update
sudo apt install -y \
  libx11-xcb1 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 \
  libxcb-render-util0 libxcb-xinerama0 libxcb-xkb1 libxcb1 libxcomposite1 \
  libxdamage1 libxfixes3 libxkbcommon-x11-0 libxrandr2 libnss3 libasound2 libgl1 \
  libqt5webengine5
```

---

## ⚙️ Build from Source (Optional)

If you prefer to build TreeCoViz on your own system (e.g., to customize features or to run on other systems), follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/frankchenfu/TreeCoViz.git
   cd TreeCoViz
   ```

2. **Create a Conda environment** using the provided `environment.yml`:

   ```bash
   conda env create -f environment.yml
   conda activate treecoviz
   ```

3. **Run the app**:

   ```bash
   python src/client.py
   ```

4. **(Optional) Build a standalone executable** using PyInstaller or NiceGUI:

   * NiceGUI (recommended):
     ```bash
     nicegui-pack --onefile --windowed --name TreeCoViz src/client.py
     ```
     
   * PyInstaller:
     ```bash
     pip install pyinstaller
     pyinstaller main.spec
     ```

   
   > ✅ Note: The executable will be placed in the `dist/` folder as `TreeCoViz` (Linux) or `TreeCoViz.exe` (Windows).

---

## ❓ Troubleshooting

**Q: Double-click does nothing on Linux?**

A: Run from terminal to capture error messages: `./TreeCoViz`

**Q: Error about missing Qt or GTK when running?**

A: Ensure the Qt dependencies listed above are installed, or try to reinstall Qt with pip.

**Q: Can I run this on MacOS?**

A: Not officially supported yet, but it may run using Python source and a suitable GUI backend. For more information, please refer to [NiceGUI Installation and Deployment](https://nicegui.io/documentation/section_configuration_deployment#package_for_installation) for MacOS.

**Q: Why does the program start slow?**

A: On first run, starting the graphical interface may be slow, especially while loading the Qt backend and initializing components. If it runs on Windows, binding dynamic links may takes longer. But after that, it works properly and runs fast.
