#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv

def main():
    """运行UberEats点餐测试"""
    # 加载环境变量
    load_dotenv()
    
    # 设置测试环境变量
    os.environ["PYTEST_ADDOPTS"] = "--headed --slowmo 100"
    
    # 运行测试
    os.system("pytest tests/test_uber_eats_order.py -v")

if __name__ == "__main__":
    main() 