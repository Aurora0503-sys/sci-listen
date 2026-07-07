#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import requests
import re

app = Flask(__name__)
CORS(app)

# ===== DeepSeek API 配置（直接嵌入密钥） =====
DEEPSEEK_API_KEY = "sk-efcf3e1387344796b490b930899744d0"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"


def generate_meeting_summary(text):
    """使用 DeepSeek API 生成会议摘要（提炼关键信息）"""
    
    if len(text) < 10:
        return ["会议内容太短，请提供更详细的会议记录"]
    
    # 直接使用嵌入的API密钥
    api_key = DEEPSEEK_API_KEY
    
    try:
        print("🔄 使用 DeepSeek API 生成会议摘要...")
        
        # 构建会议摘要提示词（不区分发言人版本）
        prompt = f"""你是一位专业的会议秘书，请对以下会议对话进行深度分析和提炼，生成结构化的会议摘要。

会议对话内容：
{text}

请按以下格式输出会议摘要（每个部分用 --- 分隔）：

一、📌 核心议题
（用1-2句话概括本次会议的核心议题，聚焦讨论的主题方向）

二、💬 关键讨论点
（按讨论主题归纳会议中涉及的关键观点和意见，用条目式列出，不要标注发言人身份）
格式示例：
- 关于[主题]：讨论认为需要...
- 关于[问题]：提出了...的解决方案

三、📋 讨论事项与决策
（列出会议中讨论的具体事项和做出的决策）

四、⚠️ 风险点与问题
（列出会议中提到的风险、问题或挑战）

五、✅ 待办事项与决议
（列出会议最终确定的任务分配和责任人）

输出要求：
1. 每个部分要简洁清晰，用条目式呈现
2. 只提取会议中实际提到的内容，不要凭空捏造
3. 如果某部分没有相关内容，标注"无"
4. 待办事项要明确具体，包含责任人和时间节点
5. 关键讨论点不要标注发言人，只归纳讨论内容本身
6. 每个条目之间要换行，保持清晰的层次结构

请输出会议摘要："""
        
        # 构建 DeepSeek API 请求
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "你是一位专业的会议秘书，擅长从会议对话中提炼关键信息，生成结构清晰、内容精炼的会议摘要。注意：不区分发言人，只归纳讨论内容本身。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.5,
            "max_tokens": 2048,
            "stream": False
        }
        
        response = requests.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )
        
        response_data = response.json()
        
        if response.status_code == 200:
            ai_text = response_data["choices"][0]["message"]["content"].strip()
            print(f"📊 DeepSeek API 返回摘要:\n{ai_text}")
            
            # 按 --- 分割各部分
            parts = re.split(r'---', ai_text)
            summary_items = []
            
            for part in parts:
                part = part.strip()
                if part:
                    summary_items.append(part)
            
            if not summary_items:
                summary_items = [ai_text]
            
            print(f"✅ 会议摘要生成成功，共 {len(summary_items)} 个部分")
            return summary_items
            
        else:
            error_msg = response_data.get('error', {}).get('message', '未知错误')
            print(f"❌ DeepSeek API 请求失败: {response.status_code} - {error_msg}")
            
            if response.status_code == 401:
                return ["API密钥无效或已过期，请联系管理员"]
            elif response.status_code == 429:
                return ["请求过于频繁，请稍后再试"]
            else:
                return [f"API请求失败: {error_msg}"]
                
    except requests.exceptions.Timeout:
        print("❌ DeepSeek API 请求超时")
        return ["请求超时，请稍后重试"]
    except Exception as e:
        print(f"❌ DeepSeek API 调用异常: {str(e)}")
        return [f"生成失败: {str(e)}"]


@app.route('/api/generate_questions', methods=['POST'])
def generate_questions():
    """API端点：生成会议摘要"""
    try:
        print(f"📥 收到请求: {request.method} {request.url}")
        
        data = request.get_json()
        if not data:
            print("❌ 错误: 无JSON数据")
            return jsonify({'error': '无效的JSON数据'}), 400
            
        text = data.get('text', '').strip()
        print(f"📝 输入文本长度: {len(text)} 字符")
        
        if not text:
            print("⚠️ 警告: 文本为空")
            return jsonify({'questions': []}), 200
        
        summary = generate_meeting_summary(text)
        print(f"✅ 生成摘要条目: {len(summary)}")
        
        response_data = {'questions': summary}
        print(f"📤 返回响应: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
        
        return jsonify(response_data), 200
        
    except Exception as e:
        error_msg = f"服务器错误: {str(e)}"
        print(f"❌ {error_msg}")
        return jsonify({'error': error_msg}), 500


@app.route('/api/answer_question', methods=['POST'])
def answer_question():
    """API端点：回答问题/提供建议"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '无效的JSON数据'}), 400
            
        question = data.get('question', '').strip()
        meeting_mode = data.get('meeting_mode', False)
        
        if not question:
            return jsonify({'error': '问题不能为空'}), 400
        
        print(f"📥 收到回答问题请求: {question[:50]}...")
        
        # 构建提示词
        if meeting_mode:
            prompt = f"""你是一位专业的会议顾问，请针对以下会议讨论要点提供深入分析和建议。

讨论要点：{question}

请从以下角度提供建议：
1. 这个要点的核心问题是什么？
2. 可能的风险和挑战有哪些？
3. 建议的解决方案或行动方向是什么？
4. 有没有需要特别关注的事项？

请给出专业、具体、可操作的建议："""
        else:
            prompt = f"""请针对以下问题进行专业回答：

问题：{question}

请给出详细、专业的回答："""
        
        # 调用 DeepSeek API
        headers = {
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "你是一位专业的会议顾问和商务分析师，擅长提供深入、可操作的建议。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2048,
            "stream": False
        }
        
        print("🔄 调用 DeepSeek API 生成建议...")
        response = requests.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code != 200:
            error_msg = f'API请求失败: {response.status_code}'
            try:
                error_detail = response.json()
                error_msg += f", {error_detail.get('error', {}).get('message', '')}"
            except:
                pass
            return jsonify({'error': error_msg}), 500
        
        result = response.json()
        answer = result["choices"][0]["message"]["content"].strip()
        
        print(f"✅ 建议生成成功，长度: {len(answer)} 字符")
        
        return jsonify({'answer': answer}), 200
        
    except requests.exceptions.Timeout:
        print("❌ DeepSeek API 请求超时")
        return jsonify({'error': '请求超时，请稍后重试'}), 500
    except Exception as e:
        error_msg = f"服务器错误: {str(e)}"
        print(f"❌ {error_msg}")
        return jsonify({'error': error_msg}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        'status': 'healthy',
        'message': 'API服务器运行正常（会议摘要模式）',
        'endpoints': ['/api/generate_questions', '/api/answer_question']
    }), 200


if __name__ == '__main__':
    print("🚀 启动会议摘要API服务器（DeepSeek版）")
    print(f"🔑 API Key: {DEEPSEEK_API_KEY[:8]}...{DEEPSEEK_API_KEY[-4:]}")
    print("📡 摘要端点: http://localhost:5002/api/generate_questions")
    print("📡 建议端点: http://localhost:5002/api/answer_question")
    print("🏥 健康检查: http://localhost:5002/health")
    print("=" * 50)
    
    try:
        app.run(host='0.0.0.0', port=5002, debug=False)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
# 在文件末尾添加这行，确保 Vercel/Railway 能找到 app
app = app