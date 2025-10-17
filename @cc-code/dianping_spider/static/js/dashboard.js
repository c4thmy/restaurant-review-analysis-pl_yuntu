// 全局变量
let currentTasks = {};
let analysisData = null;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializePage();
    loadDataFiles();
    setupEventListeners();
});

// 初始化页面
function initializePage() {
    console.log('Dashboard initialized');
}

// 设置事件监听器
function setupEventListeners() {
    // 爬取表单提交
    document.getElementById('crawlForm').addEventListener('submit', function(e) {
        e.preventDefault();
        startCrawling();
    });

    // 分析按钮
    document.getElementById('analyzeBtn').addEventListener('click', startAnalyzing);

    // 词云生成按钮
    document.getElementById('wordcloudBtn').addEventListener('click', startWordcloudGeneration);

    // 刷新文件列表按钮
    document.getElementById('refreshFilesBtn').addEventListener('click', loadDataFiles);
}

// 开始爬取
function startCrawling() {
    const restaurantName = document.getElementById('restaurantName').value.trim();
    const city = document.getElementById('city').value;
    const months = parseInt(document.getElementById('months').value);

    if (!restaurantName) {
        alert('请输入餐厅名称');
        return;
    }

    const data = {
        restaurant_name: restaurantName,
        city: city,
        months: months
    };

    // 显示进度条
    showProgress('crawl', 0, '正在提交任务...');

    fetch('/api/crawl', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentTasks.crawl = data.task_id;
            monitorTask(data.task_id, 'crawl');
        } else {
            hideProgress('crawl');
            alert('提交任务失败: ' + data.error);
        }
    })
    .catch(error => {
        hideProgress('crawl');
        console.error('Error:', error);
        alert('请求失败: ' + error.message);
    });
}

// 开始分析
function startAnalyzing() {
    const filename = document.getElementById('commentFile').value;

    if (!filename) {
        alert('请选择评论文件');
        return;
    }

    const data = {
        filename: filename
    };

    showProgress('analyze', 0, '正在提交分析任务...');

    fetch('/api/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentTasks.analyze = data.task_id;
            monitorTask(data.task_id, 'analyze');
        } else {
            hideProgress('analyze');
            alert('提交分析任务失败: ' + data.error);
        }
    })
    .catch(error => {
        hideProgress('analyze');
        console.error('Error:', error);
        alert('请求失败: ' + error.message);
    });
}

// 开始词云生成
function startWordcloudGeneration() {
    const analysisFilename = document.getElementById('analysisFile').value;

    if (!analysisFilename) {
        alert('请选择分析文件');
        return;
    }

    const data = {
        analysis_filename: analysisFilename
    };

    showProgress('wordcloud', 0, '正在提交词云生成任务...');

    fetch('/api/wordcloud', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentTasks.wordcloud = data.task_id;
            monitorTask(data.task_id, 'wordcloud');
        } else {
            hideProgress('wordcloud');
            alert('提交词云生成任务失败: ' + data.error);
        }
    })
    .catch(error => {
        hideProgress('wordcloud');
        console.error('Error:', error);
        alert('请求失败: ' + error.message);
    });
}

// 监控任务状态
function monitorTask(taskId, taskType) {
    const interval = setInterval(() => {
        fetch(`/api/task_status/${taskId}`)
        .then(response => response.json())
        .then(data => {
            updateProgress(taskType, data.progress || 0, data.message || '');

            if (data.status === 'completed') {
                clearInterval(interval);
                handleTaskCompletion(taskType, data);
            } else if (data.status === 'failed') {
                clearInterval(interval);
                hideProgress(taskType);
                alert(`任务失败: ${data.error}`);
            }
        })
        .catch(error => {
            console.error('监控任务状态失败:', error);
        });
    }, 2000); // 每2秒检查一次
}

// 处理任务完成
function handleTaskCompletion(taskType, data) {
    hideProgress(taskType);

    switch (taskType) {
        case 'crawl':
            const result = data.result;
            alert(`爬取完成！获取了 ${result.comment_count} 条评论`);
            loadDataFiles(); // 刷新文件列表
            break;

        case 'analyze':
            const analysisResult = data.result;
            alert('分析完成！');
            loadDataFiles(); // 刷新文件列表
            displayAnalysisResults(analysisResult.analysis_results);
            break;

        case 'wordcloud':
            const wordcloudResult = data.result;
            alert('词云生成完成！');
            displayWordclouds(wordcloudResult);
            break;
    }
}

// 显示进度条
function showProgress(type, progress, message) {
    const progressContainer = document.getElementById(`${type}Progress`);
    const progressBar = document.getElementById(`${type}ProgressBar`);
    const progressText = document.getElementById(`${type}ProgressText`);
    const messageDiv = document.getElementById(`${type}Message`);

    progressContainer.style.display = 'block';
    progressBar.style.width = `${progress}%`;
    progressText.textContent = `${progress}%`;
    messageDiv.textContent = message;
}

// 更新进度
function updateProgress(type, progress, message) {
    const progressBar = document.getElementById(`${type}ProgressBar`);
    const progressText = document.getElementById(`${type}ProgressText`);
    const messageDiv = document.getElementById(`${type}Message`);

    progressBar.style.width = `${progress}%`;
    progressText.textContent = `${progress}%`;
    if (message) {
        messageDiv.textContent = message;
    }
}

// 隐藏进度条
function hideProgress(type) {
    const progressContainer = document.getElementById(`${type}Progress`);
    progressContainer.style.display = 'none';
}

// 加载数据文件列表
function loadDataFiles() {
    fetch('/api/data_files')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateFileSelects(data.comment_files, data.analysis_files);
            updateFilesList(data.comment_files, data.analysis_files);
        }
    })
    .catch(error => {
        console.error('加载文件列表失败:', error);
    });
}

// 更新文件选择下拉框
function updateFileSelects(commentFiles, analysisFiles) {
    const commentSelect = document.getElementById('commentFile');
    const analysisSelect = document.getElementById('analysisFile');

    // 更新评论文件选择
    commentSelect.innerHTML = '<option value="">请选择评论文件</option>';
    commentFiles.forEach(file => {
        const option = document.createElement('option');
        option.value = file;
        option.textContent = file;
        commentSelect.appendChild(option);
    });

    // 更新分析文件选择
    analysisSelect.innerHTML = '<option value="">请选择分析文件</option>';
    analysisFiles.forEach(file => {
        const option = document.createElement('option');
        option.value = file;
        option.textContent = file;
        analysisSelect.appendChild(option);
    });
}

// 更新文件列表显示
function updateFilesList(commentFiles, analysisFiles) {
    const commentList = document.getElementById('commentFilesList');
    const analysisList = document.getElementById('analysisFilesList');

    // 显示评论文件
    if (commentFiles.length > 0) {
        commentList.innerHTML = commentFiles.map(file => `
            <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="text-truncate">${file}</span>
                <a href="/download/${file}" class="btn btn-sm btn-outline-primary">
                    <i class="fas fa-download"></i>
                </a>
            </div>
        `).join('');
    } else {
        commentList.innerHTML = '<p class="text-muted">暂无文件</p>';
    }

    // 显示分析文件
    if (analysisFiles.length > 0) {
        analysisList.innerHTML = analysisFiles.map(file => `
            <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="text-truncate">${file}</span>
                <div>
                    <button class="btn btn-sm btn-outline-info me-1" onclick="loadAnalysisResult('${file}')">
                        <i class="fas fa-eye"></i>
                    </button>
                    <a href="/download/${file}" class="btn btn-sm btn-outline-primary">
                        <i class="fas fa-download"></i>
                    </a>
                </div>
            </div>
        `).join('');
    } else {
        analysisList.innerHTML = '<p class="text-muted">暂无文件</p>';
    }
}

// 加载并显示分析结果
function loadAnalysisResult(filename) {
    fetch(`/api/analysis_result/${filename}`)
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayAnalysisResults(data.data);
        } else {
            alert('加载分析结果失败: ' + data.error);
        }
    })
    .catch(error => {
        console.error('加载分析结果失败:', error);
        alert('加载分析结果失败: ' + error.message);
    });
}

// 显示分析结果
function displayAnalysisResults(data) {
    analysisData = data;

    // 显示基础统计
    const stats = data.basic_stats;
    document.getElementById('totalComments').textContent = stats.total_comments;
    document.getElementById('avgRating').textContent = stats.average_rating;
    document.getElementById('uniqueUsers').textContent = stats.unique_users;
    document.getElementById('avgLength').textContent = Math.round(stats.average_length);

    // 显示情感分析图表
    displaySentimentChart(data.sentiments);

    // 显示交互式词云
    displayInteractiveWordcloud(data.keywords);

    // 显示分类分析
    displayCategoryChart(data.labels);

    // 显示结果区域
    document.getElementById('resultsSection').style.display = 'block';
}

// 显示情感分析图表
function displaySentimentChart(sentiments) {
    const chart = echarts.init(document.getElementById('sentimentChart'));

    const option = {
        title: {
            text: '情感分布',
            left: 'center'
        },
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            data: ['正面', '中性', '负面']
        },
        series: [
            {
                name: '情感分布',
                type: 'pie',
                radius: '50%',
                data: [
                    { value: sentiments.distribution.positive || 0, name: '正面' },
                    { value: sentiments.distribution.neutral || 0, name: '中性' },
                    { value: sentiments.distribution.negative || 0, name: '负面' }
                ],
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };

    chart.setOption(option);
}

// 显示交互式词云
function displayInteractiveWordcloud(keywords) {
    const chart = echarts.init(document.getElementById('interactiveWordcloud'));

    const data = keywords.map(([word, score]) => ({
        name: word,
        value: Math.round(score * 1000)
    }));

    const option = {
        title: {
            text: '关键词云图',
            left: 'center'
        },
        tooltip: {
            show: true
        },
        series: [{
            type: 'wordCloud',
            gridSize: 2,
            sizeRange: [12, 50],
            rotationRange: [-90, 90],
            shape: 'pentagon',
            width: '100%',
            height: '100%',
            drawOutOfBound: false,
            textStyle: {
                fontFamily: 'sans-serif',
                fontWeight: 'bold',
                color: function () {
                    return 'rgb(' + [
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160)
                    ].join(',') + ')';
                }
            },
            emphasis: {
                textStyle: {
                    shadowBlur: 10,
                    shadowColor: '#333'
                }
            },
            data: data
        }]
    };

    chart.setOption(option);
}

// 显示分类分析图表
function displayCategoryChart(labels) {
    const chart = echarts.init(document.getElementById('categoryChart'));

    const categories = Object.keys(labels.category_counts);
    const counts = Object.values(labels.category_counts);

    const option = {
        title: {
            text: '标签分类统计',
            left: 'center'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: categories,
            axisTick: {
                alignWithLabel: true
            }
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name: '提及次数',
                type: 'bar',
                barWidth: '60%',
                data: counts,
                itemStyle: {
                    color: function(params) {
                        const colors = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de'];
                        return colors[params.dataIndex % colors.length];
                    }
                }
            }
        ]
    };

    chart.setOption(option);
}

// 显示词云图
function displayWordclouds(wordcloudResult) {
    const gallery = document.getElementById('wordcloudGallery');

    // 显示总体词云
    if (wordcloudResult.overall_wordcloud) {
        const overallDiv = document.createElement('div');
        overallDiv.className = 'wordcloud-container mb-4';
        overallDiv.innerHTML = `
            <h5>整体词云图</h5>
            <img src="data:image/png;base64,${wordcloudResult.overall_wordcloud.image_base64}"
                 class="wordcloud-image" alt="整体词云图">
        `;
        gallery.appendChild(overallDiv);
    }

    // 显示分类词云
    if (wordcloudResult.category_wordclouds) {
        const categoriesDiv = document.createElement('div');
        categoriesDiv.innerHTML = '<h5>分类词云图</h5>';

        const row = document.createElement('div');
        row.className = 'row';

        Object.entries(wordcloudResult.category_wordclouds).forEach(([category, result]) => {
            const col = document.createElement('div');
            col.className = 'col-md-6 mb-3';
            col.innerHTML = `
                <div class="wordcloud-container">
                    <h6>${category}</h6>
                    <img src="data:image/png;base64,${result.image_base64}"
                         class="wordcloud-image" alt="${category}词云图">
                </div>
            `;
            row.appendChild(col);
        });

        categoriesDiv.appendChild(row);
        gallery.appendChild(categoriesDiv);
    }

    // 显示词云区域
    document.getElementById('wordcloudSection').style.display = 'block';
}

// 响应式调整
window.addEventListener('resize', function() {
    // 重新调整图表大小
    setTimeout(() => {
        if (window.echarts) {
            echarts.getInstanceByDom(document.getElementById('sentimentChart'))?.resize();
            echarts.getInstanceByDom(document.getElementById('interactiveWordcloud'))?.resize();
            echarts.getInstanceByDom(document.getElementById('categoryChart'))?.resize();
        }
    }, 100);
});