#!/bin/bash
# Start n8n backend service

cd "$(dirname "$0")"

echo "=========================================="
echo "Starting n8n Backend"
echo "=========================================="
echo ""

# Check if n8n is installed
if ! command -v n8n &> /dev/null; then
    echo "⚠️  n8n not found. Installing..."
    echo ""
    echo "Option 1: Install via npm"
    echo "  npm install -g n8n"
    echo ""
    echo "Option 2: Use Docker"
    echo "  docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n"
    echo ""
    echo "Option 3: Use n8n cloud (already configured)"
    echo "  The system will use n8n MCP server if available"
    echo ""
    exit 1
fi

echo "Starting n8n on port 5678..."
echo "Web UI: http://localhost:5678"
echo ""
echo "To import workflow:"
echo "  1. Open http://localhost:5678"
echo "  2. Go to Workflows > Import from File"
echo "  3. Select: n8n_enhanced_workflow.json"
echo "  4. Activate the workflow"
echo ""

n8n start


