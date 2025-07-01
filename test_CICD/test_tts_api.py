# test_tts_api.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import numpy as np
import base64
import io

# Import đối tượng 'app' từ file API của bạn
# Hãy đảm bảo tên file là chính xác (ví dụ: tts_api_main.py)
from Container_Folder.Text_to_Speech.TTS_API import app

# Tạo một client để gửi request giả lập đến app
client = TestClient(app)

# --- Test Case 1: Trường hợp thành công ---

# Chúng ta sử dụng @patch để "chặn" và thay thế các hàm ngoại vi.
# Điều này giúp cô lập logic API của bạn để kiểm tra.
@patch('Container_Folder.Text_to_Speech.TTS_API.LFinference')
@patch('Container_Folder.Text_to_Speech.TTS_API.torch.randn')
def test_transcribe_success(mock_torch_randn, mock_LFinference):
    """
    Kiểm tra endpoint hoạt động đúng với input hợp lệ.
    - Mock model LFinference để trả về dữ liệu âm thanh giả.
    - Mock torch.randn để không phụ thuộc vào thư viện torch.
    """
    # 1. --- Thiết lập Mock (Arrange) ---
    
    # Giả lập model LFinference trả về một mảng numpy (sóng âm giả) và một state.
    # Điều này cho phép chúng ta kiểm tra logic mà không cần chạy model thật.
    fake_audio_wave = np.array([0.1, 0.2, 0.3], dtype=np.float32)
    fake_s_prev = "fake_state"
    mock_LFinference.return_value = (fake_audio_wave, fake_s_prev)

    # Giả lập torch.randn trả về một tensor giả.
    mock_torch_randn.return_value = "fake_tensor"

    # Dữ liệu đầu vào cho API
    input_text = "Câu đầu tiên. Câu thứ hai."

    # 2. --- Hành động (Act) ---
    
    # Gửi một request POST đến endpoint với dữ liệu form.
    response = client.post("/transcribe", data={"text_input": input_text})

    # 3. --- Kiểm tra (Assert) ---

    # Kiểm tra status code có phải là 200 OK không.
    assert response.status_code == 200

    # Kiểm tra xem LFinference có được gọi 2 lần không (vì có 2 câu).
    assert mock_LFinference.call_count == 2
    
    # Kiểm tra xem LFinference có được gọi với các tham số đúng không.
    # call_args.args[0] là tham số vị trí đầu tiên (text).
    first_call_text = mock_LFinference.call_args_list[0].args[0]
    second_call_text = mock_LFinference.call_args_list[1].args[0]
    assert first_call_text == "Câu đầu tiên."
    assert second_call_text == " Câu thứ hai."

    # Kiểm tra nội dung response.
    response_json = response.json()
    assert "output_sound" in response_json

    # Giải mã base64 để xác thực nội dung âm thanh (tùy chọn nhưng rất tốt).
    decoded_audio = base64.b64decode(response_json["output_sound"])
    
    # Tạo lại file âm thanh mong đợi từ các sóng âm giả.
    expected_full_audio = np.concatenate([fake_audio_wave, fake_audio_wave])
    expected_buffer = io.BytesIO()
    import soundfile as sf
    sf.write(expected_buffer, expected_full_audio, samplerate=24000, format='WAV')
    expected_bytes = expected_buffer.getvalue()

    assert decoded_audio == expected_bytes


# --- Test Case 2: Trường hợp Model gặp lỗi ---
@patch('Container_Folder.Text_to_Speech.TTS_API.LFinference', side_effect=Exception("Model failed to load"))
def test_transcribe_model_exception(mock_LFinference):
    """
    Kiểm tra API trả về lỗi 500 khi model LFinference gặp sự cố.
    `side_effect` được dùng để khiến mock ném ra một Exception.
    """
    # Gửi request
    response = client.post("/transcribe", data={"text_input": "Một câu bất kỳ."})

    # Kiểm tra
    assert response.status_code == 500
    assert response.json() == {"error": "Model failed to load"}


# --- Test Case 3: Trường hợp Input không hợp lệ ---

def test_transcribe_missing_input():
    """
    Kiểm tra API trả về lỗi khi không có 'text_input' được cung cấp.
    FastAPI sẽ tự động xử lý và trả về lỗi 422 Unprocessable Entity.
    """
    # Gửi request với 'data' rỗng
    response = client.post("/transcribe", data={})

    # Kiểm tra
    assert response.status_code == 422
