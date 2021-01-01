mkdir -p ~/.streamlit/
echo "[general]
email = \"kirti21041999@gmail.com@com\"
" > ~/.streamlit/credentials.toml
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml