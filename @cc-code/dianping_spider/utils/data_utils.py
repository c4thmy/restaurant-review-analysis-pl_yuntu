import os
import json
import pandas as pd
from datetime import datetime
import logging


class DataManager:
    """数据管理工具类"""

    def __init__(self, data_dir='data', backup_dir='backup'):
        self.data_dir = data_dir
        self.backup_dir = backup_dir
        self.ensure_dirs()

    def ensure_dirs(self):
        """确保目录存在"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)

    def save_json(self, data, filename):
        """保存JSON数据"""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filepath

    def load_json(self, filename):
        """加载JSON数据"""
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    def save_csv(self, data, filename):
        """保存CSV数据"""
        filepath = os.path.join(self.data_dir, filename)
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = data
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        return filepath

    def load_csv(self, filename):
        """加载CSV数据"""
        filepath = os.path.join(self.data_dir, filename)
        try:
            return pd.read_csv(filepath, encoding='utf-8-sig')
        except FileNotFoundError:
            return None

    def backup_file(self, filename):
        """备份文件"""
        src = os.path.join(self.data_dir, filename)
        if os.path.exists(src):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"{timestamp}_{filename}"
            dst = os.path.join(self.backup_dir, backup_name)
            import shutil
            shutil.copy2(src, dst)
            return dst
        return None

    def list_files(self, extension=None):
        """列出数据目录中的文件"""
        files = os.listdir(self.data_dir)
        if extension:
            files = [f for f in files if f.endswith(extension)]
        return files


class Logger:
    """日志管理工具"""

    @staticmethod
    def setup(name, log_file='app.log', level=logging.INFO):
        """设置日志"""
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # 清除已有的处理器
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        # 文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger


class RateLimiter:
    """请求频率限制器"""

    def __init__(self, min_delay=1, max_delay=3):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.last_request = 0

    def wait(self):
        """等待适当时间"""
        import time
        import random

        current_time = time.time()
        elapsed = current_time - self.last_request
        delay = random.uniform(self.min_delay, self.max_delay)

        if elapsed < delay:
            sleep_time = delay - elapsed
            time.sleep(sleep_time)

        self.last_request = time.time()


class ProgressTracker:
    """进度跟踪器"""

    def __init__(self, total, desc="Progress"):
        self.total = total
        self.current = 0
        self.desc = desc

    def update(self, step=1):
        """更新进度"""
        self.current += step
        percentage = (self.current / self.total) * 100
        print(f"\r{self.desc}: {self.current}/{self.total} ({percentage:.1f}%)", end="")
        if self.current >= self.total:
            print()  # 换行

    def finish(self):
        """完成进度"""
        self.current = self.total
        self.update(0)


def clean_text(text):
    """清理文本"""
    import re

    if not text:
        return ""

    # 移除多余的空白字符
    text = re.sub(r'\s+', ' ', text)

    # 移除特殊字符（保留中文、英文、数字和常用标点）
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s，。！？；：""''（）【】、]', '', text)

    # 移除首尾空白
    text = text.strip()

    return text


def format_time(timestamp):
    """格式化时间"""
    if isinstance(timestamp, str):
        try:
            dt = datetime.fromisoformat(timestamp)
        except ValueError:
            return timestamp
    elif isinstance(timestamp, datetime):
        dt = timestamp
    else:
        return str(timestamp)

    return dt.strftime('%Y-%m-%d %H:%M:%S')


def ensure_dir(path):
    """确保目录存在"""
    os.makedirs(path, exist_ok=True)


def safe_filename(filename):
    """生成安全的文件名"""
    import re
    # 替换不安全的字符
    safe_chars = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return safe_chars


def get_file_size(filepath):
    """获取文件大小（格式化）"""
    try:
        size = os.path.getsize(filepath)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    except OSError:
        return "Unknown"