"""Role 4 application entry point for the Chatbot Baseline and ReAct Agent."""

import json
import os
import sys

from dotenv import load_dotenv


SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Import các thành phần từ file của Role 2, Role 3 & Multi-Provider Adapter
from agent_core import run_react_agent as run_react_loop
from tools import AVAILABLE_TOOLS
from prompts import CHATBOT_BASELINE_PROMPT, REACT_SYSTEM_PROMPT, MAX_ITERATIONS
from providers import get_llm_provider

load_dotenv()


def load_test_cases():
    """Đọc bộ test cases do Role 1 quản lý từ config/test_cases.json."""
    config_path = os.path.join(os.path.dirname(SRC_DIR), "config", "test_cases.json")
    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)


def run_baseline_chatbot(user_query: str, provider):
    """Chạy đúng một LLM call, tuyệt đối không đăng ký hoặc gọi tool."""
    print(f"\n💬 [CHATBOT BASELINE] Câu hỏi: {user_query}")
    response = provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT).strip()
    print(f"🤖 Chatbot trả lời:\n{response}")
    return {"answer": response, "tool_calls": 0}


def run_react_agent(user_query: str, provider):
    """Integrate Role 2 tools and Role 3 prompts through the ReAct core."""
    print(f"\n🤖 [REACT AGENT] Câu hỏi: {user_query}")
    print(f"🛠️ Agent đang có {len(AVAILABLE_TOOLS)} tool: {', '.join(AVAILABLE_TOOLS)}")
    print(f"🛡️ Guardrail: tối đa {MAX_ITERATIONS} vòng lặp")

    result = run_react_loop(
        user_query=user_query,
        provider=provider,
        tools=AVAILABLE_TOOLS,
        system_prompt=REACT_SYSTEM_PROMPT,
        max_iterations=MAX_ITERATIONS,
    )

    for item in result["trace"]:
        print(f"\n--- 🔄 Vòng lặp ReAct (Step {item['step']}/{MAX_ITERATIONS}) ---")
        if item["thought"]:
            print(f"🧠 Thought: {item['thought']}")
        print(f"🛠️ Action: {item['name']}[{', '.join(item['arguments'])}]")
        print(f"👁️ Observation: {item['observation']}")

    if result["termination_reason"] == "max_iterations":
        print(f"\n🛡️ GUARDRAIL TRIGGERED: Đã đạt giới hạn {MAX_ITERATIONS} vòng lặp.")
    print(f"\n🏁 Final Answer: {result['answer']}")
    print(f"📊 Tool calls: {result['tool_calls']}")
    return result


if __name__ == "__main__":
    print("=" * 50)
    print("🏫 ĐẠI HỌC VINUNI - BÀI LAB 3: CHATBOT VS REACT AGENT")
    print("=" * 50)

    provider = get_llm_provider()
    model_name = getattr(provider, "model_name", "Offline Mock Mode")
    print(f"🔌 LLM Provider đang hoạt động: {provider.__class__.__name__} (Model: {model_name})")

    tests = load_test_cases()
    print(f"✅ Đã tải thành công {len(tests)} Test Cases từ config/test_cases.json\n")
    
    # Tra test case theo id (không dùng chỉ số mảng, để Role 1 thêm/bớt câu vẫn chạy đúng)
    sample = next((t for t in tests if t.get("id") == 3), tests[0])
    sample_query = sample["question"]
    
    print("--- DEMO 1: CHẠY TRÊN CHATBOT BASELINE ---")
    run_baseline_chatbot(sample_query, provider)
    
    print("\n--- DEMO 2: CHẠY TRÊN REACT AGENT ---")
    run_react_agent(sample_query, provider)
