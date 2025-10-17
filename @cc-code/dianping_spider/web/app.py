from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from datetime import datetime
import threading
import queue

from config import WEB_CONFIG
from spiders.dianping_spider import DianpingSpider
from utils.text_analyzer import CommentAnalyzer
from utils.wordcloud_generator import WordCloudGenerator
from utils.data_utils import DataManager, Logger


app = Flask(__name__)
logger = Logger.setup(__name__)

# 全局变量
data_manager = DataManager()
analyzer = CommentAnalyzer()
wordcloud_gen = WordCloudGenerator()

# 任务队列
task_queue = queue.Queue()
task_results = {}


class TaskRunner:
    """后台任务运行器"""

    def __init__(self):
        self.running = False
        self.thread = None

    def start(self):
        """启动后台任务处理"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.process_tasks)
            self.thread.daemon = True
            self.thread.start()
            logger.info("后台任务处理器已启动")

    def stop(self):
        """停止后台任务处理"""
        self.running = False
        if self.thread:
            self.thread.join()
        logger.info("后台任务处理器已停止")

    def process_tasks(self):
        """处理任务队列"""
        while self.running:
            try:
                if not task_queue.empty():
                    task = task_queue.get(timeout=1)
                    self.execute_task(task)
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"处理任务失败: {e}")

    def execute_task(self, task):
        """执行具体任务"""
        task_id = task['id']
        task_type = task['type']

        try:
            task_results[task_id] = {'status': 'running', 'progress': 0}

            if task_type == 'crawl_comments':
                self.crawl_comments_task(task_id, task['params'])
            elif task_type == 'analyze_comments':
                self.analyze_comments_task(task_id, task['params'])
            elif task_type == 'generate_wordcloud':
                self.generate_wordcloud_task(task_id, task['params'])

            task_results[task_id]['status'] = 'completed'
            task_results[task_id]['progress'] = 100

        except Exception as e:
            logger.error(f"任务执行失败: {task_id}, {e}")
            task_results[task_id] = {
                'status': 'failed',
                'error': str(e),
                'progress': 0
            }

    def crawl_comments_task(self, task_id, params):
        """爬取评论任务"""
        spider = DianpingSpider()

        task_results[task_id]['progress'] = 20
        task_results[task_id]['message'] = '正在搜索餐厅...'

        # 搜索餐厅
        restaurants = spider.search_restaurant(
            params['restaurant_name'],
            params.get('city', '北京')
        )

        if not restaurants:
            raise Exception("未找到目标餐厅")

        task_results[task_id]['progress'] = 40
        task_results[task_id]['message'] = '正在获取评论...'

        # 获取评论
        comments = spider.get_restaurant_comments(
            restaurants[0]['url'],
            params.get('months', 3)
        )

        task_results[task_id]['progress'] = 80
        task_results[task_id]['message'] = '正在保存数据...'

        # 保存数据
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"comments_{params['restaurant_name']}_{timestamp}.json"
        filepath = data_manager.save_json(comments, filename)

        task_results[task_id]['result'] = {
            'filename': filename,
            'filepath': filepath,
            'comment_count': len(comments)
        }
        task_results[task_id]['message'] = f'成功获取{len(comments)}条评论'

    def analyze_comments_task(self, task_id, params):
        """分析评论任务"""
        filename = params['filename']

        task_results[task_id]['progress'] = 20
        task_results[task_id]['message'] = '正在加载评论数据...'

        # 加载评论数据
        comments = data_manager.load_json(filename)
        if not comments:
            raise Exception("评论数据加载失败")

        task_results[task_id]['progress'] = 60
        task_results[task_id]['message'] = '正在分析评论...'

        # 分析评论
        analysis_results = analyzer.analyze_comments(comments)

        task_results[task_id]['progress'] = 90
        task_results[task_id]['message'] = '正在保存分析结果...'

        # 保存分析结果
        analysis_filename = filename.replace('.json', '_analysis.json')
        analysis_filepath = data_manager.save_json(analysis_results, analysis_filename)

        task_results[task_id]['result'] = {
            'analysis_filename': analysis_filename,
            'analysis_filepath': analysis_filepath,
            'analysis_results': analysis_results
        }
        task_results[task_id]['message'] = '评论分析完成'

    def generate_wordcloud_task(self, task_id, params):
        """生成词云任务"""
        analysis_filename = params['analysis_filename']

        task_results[task_id]['progress'] = 20
        task_results[task_id]['message'] = '正在加载分析数据...'

        # 加载分析数据
        analysis_results = data_manager.load_json(analysis_filename)
        if not analysis_results:
            raise Exception("分析数据加载失败")

        task_results[task_id]['progress'] = 60
        task_results[task_id]['message'] = '正在生成词云图...'

        # 生成总体词云
        keywords = analysis_results.get('keywords', [])
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        overall_wordcloud = wordcloud_gen.generate_wordcloud(
            keywords=keywords,
            title="评论关键词云图",
            save_path=f"data/wordcloud_overall_{timestamp}.png"
        )

        task_results[task_id]['progress'] = 80
        task_results[task_id]['message'] = '正在生成分类词云...'

        # 生成分类词云
        category_keywords = analysis_results.get('labels', {}).get('category_keywords', {})
        category_wordclouds = wordcloud_gen.generate_category_wordclouds(
            category_keywords,
            save_dir=f"data/category_wordclouds_{timestamp}"
        )

        task_results[task_id]['result'] = {
            'overall_wordcloud': overall_wordcloud,
            'category_wordclouds': category_wordclouds,
            'interactive_data': wordcloud_gen.generate_interactive_wordcloud(keywords)
        }
        task_results[task_id]['message'] = '词云图生成完成'


# 创建任务运行器
task_runner = TaskRunner()


@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """仪表板"""
    # 获取可用的数据文件
    comment_files = [f for f in data_manager.list_files('.json') if 'comments_' in f and '_analysis' not in f]
    analysis_files = [f for f in data_manager.list_files('.json') if '_analysis.json' in f]

    return render_template('dashboard.html', {
        'comment_files': comment_files,
        'analysis_files': analysis_files
    })


@app.route('/api/crawl', methods=['POST'])
def api_crawl():
    """API: 开始爬取"""
    try:
        data = request.get_json()
        task_id = f"crawl_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        task = {
            'id': task_id,
            'type': 'crawl_comments',
            'params': {
                'restaurant_name': data.get('restaurant_name', ''),
                'city': data.get('city', '北京'),
                'months': data.get('months', 3)
            }
        }

        task_queue.put(task)
        task_results[task_id] = {'status': 'queued', 'progress': 0}

        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': '爬取任务已加入队列'
        })

    except Exception as e:
        logger.error(f"API爬取失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API: 开始分析"""
    try:
        data = request.get_json()
        task_id = f"analyze_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        task = {
            'id': task_id,
            'type': 'analyze_comments',
            'params': {
                'filename': data.get('filename', '')
            }
        }

        task_queue.put(task)
        task_results[task_id] = {'status': 'queued', 'progress': 0}

        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': '分析任务已加入队列'
        })

    except Exception as e:
        logger.error(f"API分析失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/wordcloud', methods=['POST'])
def api_wordcloud():
    """API: 生成词云"""
    try:
        data = request.get_json()
        task_id = f"wordcloud_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        task = {
            'id': task_id,
            'type': 'generate_wordcloud',
            'params': {
                'analysis_filename': data.get('analysis_filename', '')
            }
        }

        task_queue.put(task)
        task_results[task_id] = {'status': 'queued', 'progress': 0}

        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': '词云生成任务已加入队列'
        })

    except Exception as e:
        logger.error(f"API词云生成失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/task_status/<task_id>')
def api_task_status(task_id):
    """API: 获取任务状态"""
    if task_id in task_results:
        return jsonify(task_results[task_id])
    else:
        return jsonify({
            'status': 'not_found',
            'error': '任务未找到'
        }), 404


@app.route('/api/data_files')
def api_data_files():
    """API: 获取数据文件列表"""
    try:
        comment_files = [f for f in data_manager.list_files('.json') if 'comments_' in f and '_analysis' not in f]
        analysis_files = [f for f in data_manager.list_files('.json') if '_analysis.json' in f]

        return jsonify({
            'success': True,
            'comment_files': comment_files,
            'analysis_files': analysis_files
        })

    except Exception as e:
        logger.error(f"获取文件列表失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analysis_result/<filename>')
def api_analysis_result(filename):
    """API: 获取分析结果"""
    try:
        analysis_data = data_manager.load_json(filename)
        if analysis_data:
            return jsonify({
                'success': True,
                'data': analysis_data
            })
        else:
            return jsonify({
                'success': False,
                'error': '文件未找到'
            }), 404

    except Exception as e:
        logger.error(f"获取分析结果失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/download/<filename>')
def download_file(filename):
    """下载文件"""
    try:
        filepath = os.path.join(data_manager.data_dir, filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            return "文件未找到", 404

    except Exception as e:
        logger.error(f"下载文件失败: {e}")
        return "下载失败", 500


def create_app():
    """创建应用"""
    # 启动后台任务处理器
    task_runner.start()

    # 确保必要目录存在
    os.makedirs('data', exist_ok=True)
    os.makedirs('backup', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)

    return app


if __name__ == '__main__':
    app = create_app()
    try:
        app.run(
            host=WEB_CONFIG['host'],
            port=WEB_CONFIG['port'],
            debug=WEB_CONFIG['debug']
        )
    finally:
        task_runner.stop()