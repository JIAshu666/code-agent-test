import os
import subprocess

def create_venv(path: str) -> str:
    """在指定目录下用 uv 创建 .venv 虚拟环境"""
    try:
        os.makedirs(path, exist_ok=True)
        # 修正：使用 uv venv .venv 并通过 cwd 指定在目标目录下执行
        subprocess.run(["uv", "venv", ".venv"], cwd=path, capture_output=True, text=True, check=True)
        return f"虚拟环境已创建于: {path}/.venv"
    except FileNotFoundError:
        return "错误：未找到 uv 命令，请先安装 uv"
    except subprocess.CalledProcessError as e:
        return f"创建虚拟环境失败：{e.stderr}"

def install_deps(path: str, packages: str) -> str:
    """在指定目录的 .venv 中使用 uv 安装依赖"""
    try:
        venv_path = os.path.join(path, ".venv")
        # 使用 -p 参数明确告诉 uv 往哪个虚拟环境里装包
        cmd = ["uv", "pip", "install", "-p", venv_path] + packages.split()
        
        result = subprocess.run(
            cmd, 
            cwd=path,             # 在项目目录下执行，方便找到 requirements.txt
            capture_output=True, 
            text=True, 
            check=True
        )
        # 截取输出，防止安装日志太长撑爆 LLM 上下文
        output = result.stdout[-500:] if len(result.stdout) > 500 else result.stdout
        return f"依赖安装成功:\n{output}"
    except subprocess.CalledProcessError as e:
        return f"依赖安装失败:\n{e.stderr}"

def read_file(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"读取错误：{str(e)}"

def write_file(path: str, content: str) -> str:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"成功写入: {path}"
    except Exception as e:
        return f"写入错误：{str(e)}"

# 映射字典
AVAILABLE_TOOLS = {
    "create_venv": create_venv,
    "install_deps": install_deps,
    "read_file": read_file,
    "write_file": write_file
}
