import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from tools import search_flights, search_hotels, calculate_budget
from dotenv import load_dotenv

# Nạp biến môi trường từ file .env
load_dotenv()

# 1. Đọc System Prompt
try:
    with open("system_prompt.txt", "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()
except FileNotFoundError:
    SYSTEM_PROMPT = "Bạn là Trợ lý Du lịch Thông minh TravelBuddy. Hãy giúp người dùng lên kế hoạch chuyến bay, khách sạn và tính toán ngân sách."

# 2. Khai báo cấu trúc State (Trạng thái của Graph)
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Khởi tạo LLM và Tools
tools_list = [search_flights, search_hotels, calculate_budget]
model_name = os.getenv("DEFAULT_MODEL")

# Sử dụng cấu hình GitHub Models (Inference AI Azure)
llm = ChatOpenAI(
    base_url="https://models.inference.ai.azure.com/", 
    model=model_name
)
llm_with_tools = llm.bind_tools(tools_list)

# 4. Định nghĩa Agent Node
def agent_node(state: AgentState):
    messages = state["messages"]
    
    # Gắn System Prompt vào đầu danh sách tin nhắn nếu chưa có
    if not any(isinstance(msg, SystemMessage) for msg in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    
    response = llm_with_tools.invoke(messages)
    
    # --- LOGGING (Để sinh viên theo dõi Agent đang làm gì) ---
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"--- [HỆ THỐNG] Gọi tool: {tc['name']}({tc['args']})")
    else:
        print("--- [HỆ THỐNG] Trả lời trực tiếp")
        
    return {"messages": [response]}

# 5. Xây dựng Sơ đồ Graph (Workflow)
builder = StateGraph(AgentState)

# Thêm các nút (Nodes)
builder.add_node("agent", agent_node)
tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

# Thiết lập luồng đi (Edges)
builder.add_edge(START, "agent")
# Quyết định: Đi tiếp vào 'tools' nếu có yêu cầu gọi hàm, hoặc kết thúc nếu là văn bản thường
builder.add_conditional_edges("agent", tools_condition)
# Sau khi chạy xong công cụ, phải quay lại Agent để tổng hợp kết quả
builder.add_edge("tools", "agent")

# Biên dịch Graph
graph = builder.compile()

# 6. Vòng lặp Chat (Chat Loop)
if __name__ == "__main__":
    print("=" * 60)
    print("   TravelBuddy - TRỢ LÝ DU LỊCH THÔNG MINH (Lab 4)")
    print("   Nhập 'exit', 'thoát', 'quit' hoặc nhấn Ctrl+C để dừng.")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\nBạn: ").strip()
            if not user_input:
                print("(!) Bạn chưa nhập câu hỏi. Vui lòng thử lại.")
                continue
            
            if user_input.lower() in ["quit", "exit", "q", "thoát", "stop", "dừng"]:
                print("\n[TravelBuddy]: Tạm biệt! Hẹn gặp lại bạn trong chuyến đi tới.")
                break
                
            print("\nTravelBuddy đang suy nghĩ...")
            
            # Thực thi Graph
            result = graph.invoke({"messages": [("human", user_input)]})
            
            # Lấy phản hồi cuối cùng của AI
            final_response = result["messages"][-1]
            print(f"\nTravelBuddy: {final_response.content}")

        except KeyboardInterrupt:
            print("\n[TravelBuddy]: Tạm biệt! Hẹn gặp lại bạn trong chuyến đi tới.")
            break
        except Exception as e:
            # Xử lý các lỗi ngoại lệ khác (Lỗi API, Mạng...)
            print(f"\n[Lỗi]: {e}")