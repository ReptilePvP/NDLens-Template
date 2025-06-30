#!/bin/bash

# OpenLens Full Application Launcher - Bash Script
# Starts both API server and web interface

set -e

# Configuration
API_PORT=8000
WEB_PORT=3000
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Functions
print_colored() {
    local color=$1
    local text=$2
    echo -e "${color}${text}${NC}"
}

print_header() {
    echo ""
    print_colored $CYAN "================================================================"
    print_colored $CYAN "                    🔍 OpenLens Full Launcher 🔍"
    print_colored $CYAN "================================================================"
    echo ""
}

check_dependencies() {
    print_colored $YELLOW "🔍 Checking dependencies..."
    
    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        python_version=$(python3 --version)
        print_colored $GREEN "✅ Python found: $python_version"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
        python_version=$(python --version)
        print_colored $GREEN "✅ Python found: $python_version"
    else
        print_colored $RED "❌ Python is not installed or not in PATH"
        print_colored $RED "Please install Python and try again"
        exit 1
    fi
    
    # Check required files
    required_files=(
        "main.py"
        "try_interface.html"
        "start_openlens_full.py"
        "selenium_lens_scraper.py"
        "bs4_small_scraper.py"
        "llm_analysis.py"
        "config.py"
    )
    
    missing_files=()
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            missing_files+=("$file")
        fi
    done
    
    if [[ ${#missing_files[@]} -gt 0 ]]; then
        print_colored $RED "❌ Missing required files:"
        for file in "${missing_files[@]}"; do
            print_colored $RED "   - $file"
        done
        exit 1
    fi
    
    print_colored $GREEN "✅ All required files found"
}

cleanup() {
    echo ""
    print_colored $YELLOW "🛑 Shutting down OpenLens..."
    print_colored $YELLOW "👋 Thanks for using OpenLens!"
    exit 0
}

show_help() {
    echo ""
    print_colored $CYAN "OpenLens Full Application Launcher"
    echo ""
    print_colored $YELLOW "Usage:"
    print_colored $NC "  ./start_openlens_full.sh                 # Start with default settings"
    print_colored $NC "  ./start_openlens_full.sh --no-browser    # Start without opening browser"
    print_colored $NC "  ./start_openlens_full.sh --api-port 8080 # Use custom API port"
    print_colored $NC "  ./start_openlens_full.sh --web-port 3001 # Use custom web port"
    echo ""
    print_colored $YELLOW "Options:"
    print_colored $NC "  --no-browser    Skip opening browser automatically"
    print_colored $NC "  --api-port      API server port (default: 8000)"
    print_colored $NC "  --web-port      Web server port (default: 3000)"
    print_colored $NC "  --help, -h      Show this help message"
    echo ""
}

start_openlens() {
    print_header
    
    check_dependencies
    
    echo ""
    print_colored $GREEN "🚀 Starting OpenLens Full Application..."
    echo ""
    print_colored $CYAN "📝 Services will be available at:"
    print_colored $NC "   - API Server: http://127.0.0.1:$API_PORT"
    print_colored $NC "   - Web Interface: http://127.0.0.1:$WEB_PORT/try_interface.html"
    echo ""
    
    if [[ "$NO_BROWSER" != "true" ]]; then
        print_colored $YELLOW "🌐 Browser will open automatically in a few seconds..."
    fi
    
    print_colored $YELLOW "⚠️  To stop the application, press Ctrl+C"
    echo ""
    print_colored $BLUE "Starting servers..."
    
    # Set trap for cleanup
    trap cleanup SIGINT SIGTERM
    
    # Start the Python script
    $PYTHON_CMD start_openlens_full.py
}

# Parse command line arguments
NO_BROWSER=false
while [[ $# -gt 0 ]]; do
    case $1 in
        --no-browser)
            NO_BROWSER=true
            shift
            ;;
        --api-port)
            API_PORT="$2"
            shift 2
            ;;
        --web-port)
            WEB_PORT="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            print_colored $RED "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Change to script directory
cd "$SCRIPT_DIR"

# Main execution
start_openlens
