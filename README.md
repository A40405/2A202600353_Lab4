# ✈️ TravelBuddy: AI Agent Trợ Lý Du Lịch Thông Minh (Lab 4)

TravelBuddy là một AI Agent được xây dựng trên framework **LangGraph**, có khả năng suy nghĩ và thực hiện chuỗi hành động phức tạp để giúp người dùng lên kế hoạch du lịch hoàn chỉnh.

## 🌟 Tính năng cốt lõi
- **Tra cứu chuyến bay:** Tìm kiếm thông tin hãng bay, giờ bay và giá vé giữa các thành phố lớn.
- **Tìm kiếm khách sạn:** Gợi ý nơi ở phù hợp dựa trên điểm đến và ngân sách, ưu tiên theo đánh giá (rating).
- **Tính toán ngân sách:** Tự động trừ chi phí đã chi tiêu để quản lý ngân sách còn lại và đưa ra cảnh báo nếu vượt mức.
- **Xử lý hội thoại thông minh:** Nhớ ngữ cảnh, biết hỏi lại khi thiếu thông tin và từ chối các yêu cầu ngoài phạm vi du lịch.

## 🛠️ Yêu cầu hệ thống
- Python 3.10 trở lên.
- Đã cài đặt Anaconda hoặc môi trường ảo (venv).
- Key truy cập API (OpenAI hoặc GitHub Models).

## 🚀 Hướng dẫn cài đặt

### 1. Cài đặt thư viện
Mở terminal (hoặc Anaconda Prompt) và chạy lệnh sau:
```bash
pip install langgraph langchain-openai python-dotenv typing-extensions
```
### 2. Cấu hình biến môi trường (.env)
Đây là bước quan trọng nhất để Agent có thể kết nối với "bộ não" LLM.

#### a. Tạo một file mới tên là .env bằng cách:

Trên Windows (Command Prompt):

    copy .env.example .env

Trên Linux/macOS hoặc Git Bash:

    cp .env.example .env

Hoặc thủ công: Chuột phải vào file .env.example -> Copy -> Paste ngay tại đó và đổi tên thành .env.

#### b. Thêm api key
    OPENAI_API_KEY=...

## 🎮 Cách sử dụng
Để bắt đầu trò chuyện với TravelBuddy, chạy lệnh:

```Bash
python agent.py
```
Các lệnh đặc biệt trong khi chat:

    exit, thoát, quit: Để dừng chương trình.

    Ctrl + C: Ngắt chương trình ngay lập tức một cách an toàn.
## 🧪 Các kịch bản kiểm thử (Test Cases)
Bạn nên thử nghiệm các câu lệnh sau để thấy sức mạnh của Agent:

    Chat thông thường: "Chào bạn, bạn có thể giúp gì cho tôi?"

    Tìm chuyến bay: "Tìm vé từ Hà Nội đi Đà Nẵng."

    Lên kế hoạch tổng thể: "Tôi ở Hà Nội, muốn đi Phú Quốc với 5 triệu. Hãy tư vấn vé máy bay và khách sạn tốt nhất."

    Kiểm tra Guardrail: "Hãy viết code Python giải bài tập toán." (Agent sẽ từ chối).