#!/bin/bash
# Quick setup and deployment script

set -e

echo "🚀 Code Review Agent - Quick Setup"
echo "=================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Setup Backend
echo -e "${BLUE}Step 1: Setting up backend...${NC}"
cd backend

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate || . venv/Scripts/activate

pip install -r requirements.txt
echo -e "${GREEN}✓ Backend dependencies installed${NC}"

# Step 2: Setup Frontend
echo -e "${BLUE}Step 2: Setting up frontend...${NC}"
cd ../frontend

if [ ! -d "node_modules" ]; then
    npm install
fi

echo -e "${GREEN}✓ Frontend dependencies installed${NC}"

# Step 3: Build frontend
echo -e "${BLUE}Step 3: Building frontend...${NC}"
npm run build
echo -e "${GREEN}✓ Frontend built${NC}"

# Step 4: Setup environment
echo -e "${BLUE}Step 4: Setting up environment...${NC}"
cd ../backend

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ Created .env file${NC}"
    echo "⚠️  Please add your OpenRouter API key to backend/.env"
else
    echo -e "${GREEN}✓ .env already exists${NC}"
fi

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Add your OpenRouter API key to backend/.env"
echo "2. Run backend: cd backend && source venv/bin/activate && python main.py"
echo "3. Run frontend: cd frontend && npm run dev"
echo "4. Open http://localhost:5173"
