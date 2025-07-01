from unittest.mock import patch, ANY

# Giả sử logic RAG của bạn nằm trong một hàm/class
# from your_chatbot_project.rag_logic import handle_query

# Hàm giả để chạy ví dụ
def handle_query(query):
    pass

# Mock đồng thời nhiều thành phần
@patch('your_chatbot_project.rag_logic.llm.generate')
@patch('your_chatbot_project.rag_logic.vector_db.search')
@patch('your_chatbot_project.rag_logic.embedding_model.embed')
def test_prompt_construction_for_llm(mock_embed, mock_db_search, mock_llm_generate):
    """
    Unit test quan trọng nhất: Kiểm tra xem prompt được xây dựng cho LLM có đúng không.
    """
    # 1. Thiết lập các Mock
    user_query = "Thời tiết ở Đà Nẵng hôm nay thế nào?"
    
    # Mock embedding model trả về một vector giả
    mock_embed.return_value = [0.1, 0.2, 0.3]
    
    # Mock vector DB trả về một vài đoạn tài liệu giả
    retrieved_docs = [
        "Thông tin thời tiết: Đà Nẵng trời nắng, nhiệt độ 30 độ C.",
        "Lịch sử Đà Nẵng: Đà Nẵng là một thành phố biển."
    ]
    mock_db_search.return_value = retrieved_docs
    
    # Mock LLM trả về một câu trả lời giả
    mock_llm_generate.return_value = "Theo thông tin tôi tìm được, trời nắng và 30 độ."

    # 2. Gọi hàm xử lý logic chính
    final_answer = handle_query(user_query)

    # 3. Kiểm tra (Assert):
    # - Hàm tìm kiếm DB có được gọi với vector giả không?
    mock_db_search.assert_called_once_with(vector=[0.1, 0.2, 0.3], top_k=ANY)

    # - Quan trọng nhất: Kiểm tra prompt đã được gửi đến LLM
    #   Lấy ra tham số mà hàm mock_llm_generate đã được gọi với nó.
    mock_llm_generate.assert_called_once()
    actual_prompt = mock_llm_generate.call_args[0][0]

    print(f"Prompt thực tế được tạo ra:\n{actual_prompt}")

    # - Prompt có chứa câu hỏi của người dùng không?
    assert user_query in actual_prompt
    # - Prompt có chứa tài liệu đã tìm được không?
    assert retrieved_docs[0] in actual_prompt
    assert retrieved_docs[1] in actual_prompt
    # - Prompt có chứa các chỉ dẫn (instructions) mà bạn đã định sẵn không?
    assert "Dựa vào thông tin sau đây để trả lời câu hỏi" in actual_prompt

