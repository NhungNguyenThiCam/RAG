import sys
import os

# Thêm thư mục gốc của dự án vào Python Path.
# Điều này cho phép pytest tìm thấy module 'Container_Folder' khi chạy test.

# Lấy đường dẫn đến thư mục chứa file conftest.py này (tức là 'test_CICD')
current_dir = os.path.dirname(__file__)

# Đi ngược lên một cấp để lấy đường dẫn thư mục gốc của dự án ('RAG_Project')
project_root = os.path.abspath(os.path.join(current_dir, '..'))

# Thêm đường dẫn gốc vào đầu danh sách tìm kiếm của Python
sys.path.insert(0, project_root)
