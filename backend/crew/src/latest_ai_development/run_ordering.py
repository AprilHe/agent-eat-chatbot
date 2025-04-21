#!/usr/bin/env python
import os
from dotenv import load_dotenv
from main import run

if __name__ == "__main__":
    # 加载环境变量
    load_dotenv()
    
    # 运行点餐系统
    run() 