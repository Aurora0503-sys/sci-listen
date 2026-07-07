#!/usr/bin/env python3

# 简单的API测试脚本
import requests
import json

def test_api():
    url = "http://localhost:5001/api/generate_questions"
    data = {
        "text": "本研究提出了一种新的深度学习框架，结合卷积神经网络和注意力机制，用于医学图像诊断。在5个公开数据集上验证，准确率达到95.6%，超过现有方法约3个百分点。"
    }
    
    try:
        print("🔍 正在测试API...")
        response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            questions = result.get('questions', [])
            
            print(f"✅ API响应成功！")
            print(f"📝 生成了 {len(questions)} 个问题：\n")
            
            for i, question in enumerate(questions, 1):
                print(f"{i}. {question}")
                
        else:
            print(f"❌ API响应错误: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API服务器")
        print("请确保服务器正在运行在 http://localhost:5001")
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_api()