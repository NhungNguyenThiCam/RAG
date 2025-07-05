#!/bin/bash
cd Container_Folder
pytest ../test_CICD/test_tts_api.py
pytest ../test_CICD/test_whisper-api.py
pytest ../test_CICD/test_chatbot_api.py
