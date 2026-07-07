#!/usr/bin/env python3
import requests
import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 模拟高质量的学术问题生成（用于测试）
def generate_mock_questions(text):
    questions = [
        f"基于您提到的关于{text[:20]}...的内容，请问该方法的理论基础是什么？在什么条件下可能失效？",
        f"该研究的实验设计是否充分考虑了对照组设置？样本量是否充足，是否进行了功效分析？",
        f"考虑到实际应用的复杂性，您提出的解决方案在资源受限环境下如何保证性能和可扩展性？"
    ]
    return questions[:3]  # 返回前3个问题

@app.route('/api/generate_questions', methods=['POST'])
def generate_questions():
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'questions': []}), 200
            
        # 使用模拟问题生成
        questions = generate_mock_questions(text)
        
        return jsonify({'questions': questions})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("测试API服务器已启动")
    print("API端点: http://localhost:5001/api/generate_questions")
    app.run(host='0.0.0.0', port=5001, debug=True)