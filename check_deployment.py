#!/usr/bin/env python3
"""
修仙游戏助手 - 部署检查工具
检查环境和配置是否正确
"""

import os
import sys
import yaml
from pathlib import Path

def check_docker():
    """检查 Docker 是否安装"""
    import subprocess
    try:
        subprocess.run(['docker', '--version'], capture_output=True, check=True)
        subprocess.run(['docker-compose', '--version'], capture_output=True, check=True)
        return True, "✅ Docker 和 Docker Compose 已安装"
    except Exception as e:
        return False, f"❌ Docker 环境问题: {e}"

def check_config():
    """检查配置文件"""
    config_path = Path('config/config.yaml')
    
    if not config_path.exists():
        return False, "❌ config/config.yaml 不存在"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # 检查必填项
        required = {
            'telegram.bot_token': '❌ bot_token 未配置',
            'telegram.user_id': '❌ user_id 未配置',
        }
        
        for key, error_msg in required.items():
            keys = key.split('.')
            value = config
            for k in keys:
                if isinstance(value, dict):
                    value = value.get(k)
                else:
                    return False, error_msg
            
            if not value or value == 'YOUR_BOT_TOKEN_HERE':
                return False, error_msg
        
        return True, "✅ 配置文件检查通过"
    
    except Exception as e:
        return False, f"❌ 配置文件格式错误: {e}"

def check_structure():
    """检查项目结构"""
    required_dirs = [
        'src/handlers',
        'src/services',
        'src/database',
        'src/utils',
        'config',
        'web',
    ]
    
    required_files = [
        'src/main.py',
        'src/bot.py',
        'Dockerfile',
        'docker-compose.yml',
        'requirements.txt',
        'README.md',
    ]
    
    missing = []
    
    for dir_path in required_dirs:
        if not Path(dir_path).is_dir():
            missing.append(f"目录缺失: {dir_path}")
    
    for file_path in required_files:
        if not Path(file_path).is_file():
            missing.append(f"文件缺失: {file_path}")
    
    if missing:
        return False, "❌ 项目结构不完整:\n  " + "\n  ".join(missing)
    
    return True, "✅ 项目结构检查通过"

def check_space():
    """检查磁盘空间"""
    import shutil
    total, used, free = shutil.disk_usage('.')
    free_gb = free / (1024**3)
    
    if free_gb < 0.5:
        return False, f"❌ 磁盘空间不足 ({free_gb:.2f}GB)"
    
    return True, f"✅ 磁盘空间充足 ({free_gb:.2f}GB)"

def main():
    """主检查流程"""
    print("=" * 50)
    print("修仙游戏助手 - 部署检查")
    print("=" * 50)
    print()
    
    checks = [
        ("Docker 环境", check_docker),
        ("项目结构", check_structure),
        ("配置文件", check_config),
        ("磁盘空间", check_space),
    ]
    
    results = []
    all_passed = True
    
    for name, check_func in checks:
        print(f"检查 {name}...", end=" ")
        sys.stdout.flush()
        
        try:
            passed, message = check_func()
            print()
            print(f"  {message}")
            results.append((name, passed, message))
            if not passed:
                all_passed = False
        except Exception as e:
            print()
            print(f"  ❌ 检查出错: {e}")
            results.append((name, False, str(e)))
            all_passed = False
        
        print()
    
    # 总结
    print("=" * 50)
    if all_passed:
        print("✅ 所有检查通过！")
        print()
        print("现在可以部署了：")
        print("  bash deploy.sh")
        return 0
    else:
        print("❌ 存在以下问题：")
        for name, passed, message in results:
            if not passed:
                print(f"  - {name}: {message}")
        print()
        print("请解决上述问题后重试")
        return 1

if __name__ == '__main__':
    sys.exit(main())
