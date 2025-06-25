#!/bin/bash

# Obesity Prediction System Startup Script
echo "🏥 Starting Obesity Prediction System..."

# Check if required files exist
if [ ! -f "best_obesity_model.pkl" ]; then
    echo "❌ Model file not found. Please run the Jupyter notebook first."
    exit 1
fi

if [ ! -f "main.py" ]; then
    echo "❌ FastAPI backend file not found."
    exit 1
fi

if [ ! -f "app.py" ]; then
    echo "❌ Streamlit frontend file not found."
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Start FastAPI backend
echo "🚀 Starting FastAPI backend on port 8000..."
python3 main.py &
FASTAPI_PID=$!

# Wait for FastAPI to start
sleep 5

# Check if FastAPI is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ FastAPI backend started successfully"
else
    echo "❌ Failed to start FastAPI backend"
    kill $FASTAPI_PID 2>/dev/null
    exit 1
fi

# Start Streamlit frontend
echo "🎨 Starting Streamlit frontend on port 8501..."
streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &
STREAMLIT_PID=$!

# Wait for Streamlit to start
sleep 10

# Check if Streamlit is running
if curl -s http://localhost:8501 > /dev/null; then
    echo "✅ Streamlit frontend started successfully"
    echo ""
    echo "🎉 System is ready!"
    echo "📊 FastAPI Backend: http://localhost:8000"
    echo "🌐 Streamlit Frontend: http://localhost:8501"
    echo "📚 API Documentation: http://localhost:8000/docs"
    echo ""
    echo "Press Ctrl+C to stop the system"
    
    # Wait for user interrupt
    trap "echo '🛑 Stopping system...'; kill $FASTAPI_PID $STREAMLIT_PID 2>/dev/null; exit 0" INT
    wait
else
    echo "❌ Failed to start Streamlit frontend"
    kill $FASTAPI_PID $STREAMLIT_PID 2>/dev/null
    exit 1
fi

