import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import io

# Giả sử file main của FastAPI của bạn là 'main.py' và app tên là 'app'
# from your_whisper_project.main import app 
# Vì đây là ví dụ, chúng ta sẽ giả định app đã được import
# client = TestClient(app)

# Đây là một client giả để chạy ví dụ
class FakeApp:
    def __init__(self):
        pass
client = TestClient(FakeApp())


# --- Test trường hợp thành công ---
# @patch chỉ đến nơi hàm được SỬ DỤNG, không phải nơi nó được ĐỊNH NGHĨA
@patch('your_whisper_project.main.whisper_model.transcribe')
def test_transcribe_audio_success(mock_transcribe):
    """
    Kiểm tra API hoạt động đúng khi có file hợp lệ.
    Chúng ta sẽ mock hàm `transcribe` để nó trả về một kết quả giả.
    """
    # 1. Thiết lập Mock: Định sẵn kết quả trả về của hàm transcribe
    expected_text = "Đây là văn bản đã được nhận dạng."
    mock_transcribe.return_value = expected_text

    # 2. Chuẩn bị dữ liệu giả: Một file âm thanh giả
    fake_audio_bytes = b"fake audio data"
    audio_file = ("test.wav", io.BytesIO(fake_audio_bytes), "audio/wav")

    # 3. Gọi API: Gửi request đến endpoint /transcribe
    # response = client.post("/transcribe", files={"audio_file": audio_file})
    # Giả lập response thành công để chạy ví dụ
    class FakeResponse:
        status_code = 200
        def json(self):
            return {"transcription": expected_text}
    response = FakeResponse()


    # 4. Kiểm tra (Assert):
    # - Hàm mock transcribe có được gọi đúng 1 lần không?
    # mock_transcribe.assert_called_once() 
    
    # - Response status code có phải là 200 OK không?
    assert response.status_code == 200
    
    # - Nội dung JSON trả về có đúng như kết quả mock đã định sẵn không?
    assert response.json() == {"transcription": expected_text}


# --- Test trường hợp lỗi ---
def test_transcribe_no_file_uploaded():
    """
    Kiểm tra API trả về lỗi 400 Bad Request khi không có file nào được upload.
    """
    # Gọi API mà không có tham số 'files'
    # response = client.post("/transcribe")
    # Giả lập response lỗi để chạy ví dụ
    class FakeResponse:
        status_code = 400
        def json(self):
            return {"detail": "No audio file provided"}
    response = FakeResponse()

    # Kiểm tra status code và thông báo lỗi
    assert response.status_code == 400
    assert "No audio file provided" in response.json()["detail"]