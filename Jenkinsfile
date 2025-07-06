// Jenkinsfile (Declarative Pipeline)

pipeline {
    agent any

    // KHỐI "WHEN" Ở CẤP CAO NHẤT ĐÃ BỊ XÓA VÌ SAI CÚ PHÁP

    environment {
        DOCKER_REGISTRY_USER = 'tructran172003' 
        
        // Tên các ảnh Docker
        TTS_IMAGE_NAME = "${env.DOCKER_REGISTRY_USER}/rag-tts-service"
        STT_IMAGE_NAME = "${env.DOCKER_REGISTRY_USER}/rag-stt-service"
        CHATBOT_IMAGE_NAME = "${env.DOCKER_REGISTRY_USER}/rag-chatbot-service"
        
        // ID của registry credential đã được lưu trong Jenkins
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'

        // SỬ DỤNG BUILD_NUMBER LÀM TAG PHIÊN BẢN
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        // Giai đoạn 1: Lấy mã nguồn từ Git
        stage('Checkout SCM') {
            steps {
                echo 'Đang lấy mã nguồn từ Git...'
                git url: 'https://github.com/TrucTranTrung/RAG_Project', branch: 'main'
            }
        }

        // Giai đoạn 2: Xây dựng các ảnh Docker
        stage('Build Docker Images') {
            // VÍ DỤ: Thêm 'when' vào đây nếu bạn muốn stage này chỉ chạy khi có thay đổi
            when {
                changeset "Container_Folder/**"
            }
            steps {
                script {
                    echo "Bắt đầu xây dựng các ảnh Docker với tag: ${IMAGE_TAG}"
                    
                    // Xây dựng ảnh cho Text-to-Speech service với tag phiên bản
                    docker.build("${TTS_IMAGE_NAME}:${IMAGE_TAG}", "-f ../RAG_Project/Container_Folder/Text_to_Speech/dockerfile .")
                    
                    // Xây dựng ảnh cho Speech-to-Text service với tag phiên bản
                    docker.build("${STT_IMAGE_NAME}:${IMAGE_TAG}", "-f ../RAG_Project/Container_Folder/Faster_Whisper/dockerfile .")

                    // Xây dựng ảnh cho Chatbot RAG service với tag phiên bản
                    docker.build("${CHATBOT_IMAGE_NAME}:${IMAGE_TAG}", "-f ../RAG_Project/Container_Folder/chatbot_api/dockerfile .")
                    
                    echo "Xây dựng ảnh Docker hoàn tất."
                }
            }
        }

        // Giai đoạn 3: Chạy các bài test bên trong một Docker container
        stage('Run Tests') {
            steps {
                script {
                    echo "Chuẩn bị môi trường test sử dụng Docker..."
                    docker.image('python:3.10-slim').inside {
                        echo "Bắt đầu chạy các bài kiểm thử (pytest) bên trong container..."
                        
                        // Cài đặt các thư viện cần thiết cho test
                        sh 'pip install -r requirements.txt'
                        
                        // Chạy các file test
                        sh './run_test.sh'
                        
                        echo "Tất cả các bài kiểm thử đã pass."
                    }
                }
            }
        }

        // Giai đoạn 4: Đẩy ảnh Docker lên Registry
        stage('Push Docker Images') {
            when {
                branch 'main'
                // Bạn cũng có thể thêm điều kiện changeset ở đây
                // changeset "Container_Folder/**"
            }
            steps {
                script {
                    echo "Đang đẩy các ảnh Docker lên Docker Hub..."
                    
                    // Đăng nhập vào Docker Hub sử dụng credential đã lưu trong Jenkins
                    docker.withRegistry("https://registry.hub.docker.com", DOCKER_CREDENTIALS_ID) {
                        
                        // Đẩy từng ảnh với tag phiên bản cụ thể
                        // docker.image("${TTS_IMAGE_NAME}:${IMAGE_TAG}").push()
                        // docker.image("${STT_IMAGE_NAME}:${IMAGE_TAG}").push()
                        // docker.image("${CHATBOT_IMAGE_NAME}:${IMAGE_TAG}").push()

                        // Đẩy thêm tag 'latest' để trỏ đến phiên bản mới nhất
                        docker.image("${TTS_IMAGE_NAME}:${IMAGE_TAG}").push("latest")
                        docker.image("${STT_IMAGE_NAME}:${IMAGE_TAG}").push("latest")
                        docker.image("${CHATBOT_IMAGE_NAME}:${IMAGE_TAG}").push("latest")
                    }
                    
                    echo "Đẩy ảnh Docker hoàn tất."
                }
            }
        }
        
        // Giai đoạn 5: Triển khai ứng dụng
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo "Bắt đầu triển khai ứng dụng phiên bản: ${IMAGE_TAG}"
                
                // placeholder.

                echo "Triển khai hoàn tất (placeholder)."
            }
        }
    }
    
    // Các hành động sẽ được thực hiện sau khi pipeline kết thúc
    post {
        always {
            echo 'Pipeline đã kết thúc.'
            cleanWs()
        }
        success {
            echo 'Pipeline thành công!'
        }
        failure {
            echo 'Pipeline thất bại!'
        }
    }
}
