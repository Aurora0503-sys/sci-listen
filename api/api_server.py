from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
import re

app = Flask(__name__)
CORS(app)

# 使用你提供的 DeepSeek API Key
DEEPSEEK_API_KEY = "sk-efcf3e1387344796b490b930899744d0"

@app.route('/')
def index():
    """提供主页服务"""
    return send_from_directory('.', 'simple_sci_listen.html')

@app.route('/api/generate_questions', methods=['POST'])
def generate_questions():
    if not DEEPSEEK_API_KEY:
        return jsonify({'error': 'DEEPSEEK_API_KEY未配置'}), 500
    
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'questions': []}), 200
        
        # 构建高质量的学术提问提示词
        prompt = f"""你是一位资深学术研究者，具备深厚的科研背景和批判性思维。请基于以下学术报告片段，生成3个具有深度和洞察力的专业问题。

学术报告内容：{text}

问题生成要求：
1. **具体深入**：避免泛泛而谈，要有具体的技术或理论切入点
2. **批判性思维**：质疑假设、挑战观点、指出潜在问题
3. **创新思维**：提出新的视角、扩展方向或改进建议
4. **学术规范**：符合学术会议提问的专业水准和表达习惯

问题类型应涵盖：
- **方法学质疑**：对研究方法、实验设计的深入质疑
- **理论挑战**：对理论基础、假设条件的挑战
- **实用性探讨**：对实际应用价值的深入思考
- **创新扩展**：提出创新性的改进或扩展方向
- **关联性思考**：与其他领域或研究的关联性分析

输出要求：
- 每个问题要有明确的针对性和深度
- 问题的表述要专业、精准、有挑战性
- 避免简单的"是什么""为什么"类型的问题
- 每个问题占一行，以中文输出

示例高质量问题：
✓ "该方法在处理非独立同分布数据时，其理论基础是否仍然成立？如果需要扩展到这种情况，算法应该如何调整？"
✓ "您提到的性能提升3.2%是否具有统计学意义？此外，在不同规模的数据集上，这种提升的一致性如何？"
✓ "考虑到模型的可解释性问题，在医疗诊断等高风险场景中，如何平衡性能提升与决策透明度的需求？"

请基于上述要求生成问题："""
        
        # 调用 DeepSeek API
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}'
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "你是一位资深学术研究者，具备深厚的科研背景和批判性思维，擅长从深度和广度分析学术研究并生成高质量的专业问题。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 1024,
            "temperature": 0.7
        }
        
        response = requests.post(
            'https://api.deepseek.com/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            error_msg = f'DeepSeek API请求失败: {response.status_code}'
            try:
                error_detail = response.json()
                error_msg += f", {error_detail.get('error', {}).get('message', '')}"
            except:
                pass
            return jsonify({'error': error_msg}), 500
        
        result = response.json()
        
        # 解析 DeepSeek 返回的问题
        ai_questions_text = result['choices'][0]['message']['content']
        lines = ai_questions_text.split('\n')
        ai_questions = []
        
        for q in lines:
            q = q.strip()
            if q:
                # 使用正则表达式去除编号和星号标记
                q = re.sub(r'^\d+\.\s*', '', q)
                q = re.sub(r'^\*\s*|\s*\*$', '', q)
                q = re.sub(r'^[-•]\s*', '', q)
                q = q.strip()
                
                # 检查是否是有效问题（包含问号）
                if q and len(q) > 3 and ('？' in q or '?' in q):
                    ai_questions.append(q)

        # 如果没有找到以问号结尾的问题，尝试从文本中提取可能的问题
        if not ai_questions:
            sentences = re.split(r'[。！!?？\n]', ai_questions_text)
            for s in sentences:
                s = s.strip()
                if len(s) > 5 and any(ques_word in s for ques_word in ['什么', '如何', '为什么', '是否', '哪个', '何时', '何地', '怎样', '为何']):
                    if not s.endswith('?') and not s.endswith('？'):
                        s += '？'
                    if s not in ai_questions:
                        ai_questions.append(s)

        # 过滤掉空问题，最多返回3个
        ai_questions = [q for q in ai_questions if q and len(q) > 3]
        if len(ai_questions) > 3:
            ai_questions = ai_questions[:3]
        
        return jsonify({'questions': ai_questions})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🎓 学术会议陪听助手API已启动")
    print(f"🔑 DeepSeek API Key: {DEEPSEEK_API_KEY[:8]}...{DEEPSEEK_API_KEY[-4:]}")
    print("📍 API端点: http://localhost:5000/api/generate_questions")
    print("🌐 访问: http://localhost:5000")
    print("按 Ctrl+C 停止服务")
    app.run(host='0.0.0.0', port=5000, debug=True)