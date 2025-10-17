# -*- coding: utf-8 -*-
"""
数据工具
Data Utilities

提供数据管理和日志功能
"""

import json
import os
import logging
from datetime import datetime

class DataManager:
    """数据管理器"""

    def load_json(self, file_path):
        """加载JSON文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载文件失败 {file_path}: {e}")
            return None

    def save_json(self, data, file_path):
        """保存JSON文件"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存文件失败 {file_path}: {e}")
            return False

class Logger:
    """日志管理器"""

    @staticmethod
    def setup(name, log_file=None):
        """设置日志器"""
        logger = logging.getLogger(name)
        if logger.handlers:
            return logger

        logger.setLevel(logging.INFO)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 文件处理器
        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            logger.addHandler(file_handler)

        # 格式化器
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        if log_file:
            file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        return logger