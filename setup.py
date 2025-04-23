import os
import subprocess
import sys
import platform
from pathlib import Path

print("🚀 Iniciando setup do Dungeon-DOOM...\n")

project_dir = Path(__file__).parent.resolve()
venv_dir = project_dir / ".venv"
is_windows = platform.system() == "Windows"

# Caminhos internos da venv
python_in_venv = venv_dir / ("Scripts/python.exe" if is_windows else "bin/python")
pip_in_venv = venv_dir / ("Scripts/pip.exe" if is_windows else "bin/pip")

# Criação da venv
print(f"🔧 Criando ambiente virtual em {venv_dir}...")
subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)

# Atualiza o pip
print("📦 Atualizando pip...")
subprocess.run([str(python_in_venv), "-m", "pip", "install", "--upgrade", "pip"], check=True)

# Instala dependências
requirements_file = project_dir / "requirements.txt"
if requirements_file.exists():
    print("🎮 Instalando dependências do requirements.txt...")
    subprocess.run([str(pip_in_venv), "install", "-r", str(requirements_file)], check=True)
else:
    print("⚠️ Arquivo requirements.txt não encontrado. Pulando instalação.")

# Rodar o jogo automaticamente
main_file = project_dir / "main.py"
if main_file.exists():
    print("🕹️ Iniciando o Dungeon-DOOM!")
    subprocess.run([str(python_in_venv), str(main_file)])
else:
    print("❌ Arquivo main.py não encontrado.")

print("\n✅ Setup concluído!")
