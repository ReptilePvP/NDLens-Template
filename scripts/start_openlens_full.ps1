# OpenLens Full Application Launcher - PowerShell Script
# Starts both API server and web interface

param(
    [switch]$NoBrowser,  # Skip opening browser automatically
    [int]$ApiPort = 8000,
    [int]$WebPort = 3000
)

# Configuration
$ErrorActionPreference = "Stop"
$Host.UI.RawUI.WindowTitle = "OpenLens - Full Application"

# Colors for output
function Write-ColoredText {
    param(
        [string]$Text,
        [ConsoleColor]$Color = "White"
    )
    Write-Host $Text -ForegroundColor $Color
}

function Write-Header {
    Write-Host ""
    Write-ColoredText "================================================================" Cyan
    Write-ColoredText "                    🔍 OpenLens Full Launcher 🔍" Cyan  
    Write-ColoredText "================================================================" Cyan
    Write-Host ""
}

function Test-Dependencies {
    Write-ColoredText "🔍 Checking dependencies..." Yellow
    
    # Check Python
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColoredText "✅ Python found: $pythonVersion" Green
        } else {
            throw "Python not found"
        }
    } catch {
        Write-ColoredText "❌ Python is not installed or not in PATH" Red
        Write-ColoredText "Please install Python and try again" Red
        exit 1
    }
    
    # Check required files
    $requiredFiles = @(
        "main.py",
        "try_interface.html", 
        "start_openlens_full.py",
        "selenium_lens_scraper.py",
        "bs4_small_scraper.py",
        "llm_analysis.py",
        "config.py"
    )
    
    $missingFiles = @()
    foreach ($file in $requiredFiles) {
        if (-not (Test-Path $file)) {
            $missingFiles += $file
        }
    }
    
    if ($missingFiles.Count -gt 0) {
        Write-ColoredText "❌ Missing required files:" Red
        foreach ($file in $missingFiles) {
            Write-ColoredText "   - $file" Red
        }
        exit 1
    }
    
    Write-ColoredText "✅ All required files found" Green
}

function Start-OpenLens {
    Write-Header
    
    Test-Dependencies
    
    Write-Host ""
    Write-ColoredText "🚀 Starting OpenLens Full Application..." Green
    Write-Host ""
    Write-ColoredText "📝 Services will be available at:" Cyan
    Write-ColoredText "   - API Server: http://127.0.0.1:$ApiPort" White
    Write-ColoredText "   - Web Interface: http://127.0.0.1:$WebPort/try_interface.html" White
    Write-Host ""
    
    if (-not $NoBrowser) {
        Write-ColoredText "🌐 Browser will open automatically in a few seconds..." Yellow
    }
    
    Write-ColoredText "⚠️  To stop the application, press Ctrl+C" Yellow
    Write-Host ""
    Write-ColoredText "Starting servers..." Magenta
    
    try {
        # Start the Python script
        python start_openlens_full.py
    } catch {
        Write-ColoredText "❌ Failed to start OpenLens: $($_.Exception.Message)" Red
        exit 1
    }
}

function Show-Help {
    Write-Host ""
    Write-ColoredText "OpenLens Full Application Launcher" Cyan
    Write-Host ""
    Write-ColoredText "Usage:" Yellow
    Write-ColoredText "  .\start_openlens_full.ps1                 # Start with default settings" White
    Write-ColoredText "  .\start_openlens_full.ps1 -NoBrowser      # Start without opening browser" White
    Write-ColoredText "  .\start_openlens_full.ps1 -ApiPort 8080   # Use custom API port" White
    Write-ColoredText "  .\start_openlens_full.ps1 -WebPort 3001   # Use custom web port" White
    Write-Host ""
    Write-ColoredText "Options:" Yellow
    Write-ColoredText "  -NoBrowser    Skip opening browser automatically" White
    Write-ColoredText "  -ApiPort      API server port (default: 8000)" White  
    Write-ColoredText "  -WebPort      Web server port (default: 3000)" White
    Write-Host ""
}

# Main execution
if ($args -contains "-h" -or $args -contains "--help" -or $args -contains "help") {
    Show-Help
    exit 0
}

try {
    Start-OpenLens
} catch {
    Write-ColoredText "❌ Unexpected error: $($_.Exception.Message)" Red
    exit 1
} finally {
    Write-Host ""
    Write-ColoredText "👋 OpenLens has been stopped" Yellow
    Write-Host ""
}
