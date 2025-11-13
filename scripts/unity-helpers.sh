#!/bin/bash
# Unity Helper Scripts for Claude Code & Developer Collaboration
# These scripts automate common Unity operations from the command line

set -e

PROJECT_PATH="/home/user/games_worldbuilder/unity-project"
UNITY_EDITOR="/Applications/Unity/Hub/Editor/2022.3.15f1/Unity.app/Contents/MacOS/Unity"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Unity is installed
check_unity() {
    if [ ! -f "$UNITY_EDITOR" ]; then
        echo -e "${RED}Unity Editor not found at: $UNITY_EDITOR${NC}"
        echo "Please update UNITY_EDITOR path in this script"
        exit 1
    fi
}

# Run Unity tests in batch mode
run_tests() {
    echo -e "${YELLOW}Running Unity tests in batch mode...${NC}"
    check_unity

    "$UNITY_EDITOR" \
        -runTests \
        -batchmode \
        -projectPath "$PROJECT_PATH" \
        -testResults "$PROJECT_PATH/test-results.xml" \
        -testPlatform PlayMode \
        -logFile "$PROJECT_PATH/test.log"

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Tests passed${NC}"
        cat "$PROJECT_PATH/test-results.xml"
    else
        echo -e "${RED}✗ Tests failed${NC}"
        cat "$PROJECT_PATH/test.log"
        exit 1
    fi
}

# Build for iOS
build_ios() {
    echo -e "${YELLOW}Building for iOS...${NC}"
    check_unity

    "$UNITY_EDITOR" \
        -quit -batchmode -nographics \
        -projectPath "$PROJECT_PATH" \
        -executeMethod BuildScript.BuildIOS \
        -logFile "$PROJECT_PATH/build-ios.log"

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ iOS build succeeded${NC}"
    else
        echo -e "${RED}✗ iOS build failed${NC}"
        cat "$PROJECT_PATH/build-ios.log"
        exit 1
    fi
}

# Build for Android
build_android() {
    echo -e "${YELLOW}Building for Android...${NC}"
    check_unity

    "$UNITY_EDITOR" \
        -quit -batchmode -nographics \
        -projectPath "$PROJECT_PATH" \
        -executeMethod BuildScript.BuildAndroid \
        -logFile "$PROJECT_PATH/build-android.log"

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Android build succeeded${NC}"
    else
        echo -e "${RED}✗ Android build failed${NC}"
        cat "$PROJECT_PATH/build-android.log"
        exit 1
    fi
}

# Validate Unity project
validate_project() {
    echo -e "${YELLOW}Validating Unity project...${NC}"

    # Check for .meta files
    echo "Checking for missing .meta files..."
    MISSING_META=0
    for file in $(find "$PROJECT_PATH/Assets" -type f ! -name "*.meta"); do
        if [ ! -f "$file.meta" ]; then
            echo -e "${RED}Missing .meta file for: $file${NC}"
            MISSING_META=1
        fi
    done

    # Check for orphaned .meta files
    echo "Checking for orphaned .meta files..."
    ORPHANED_META=0
    for meta in $(find "$PROJECT_PATH/Assets" -type f -name "*.meta"); do
        original="${meta%.meta}"
        if [ ! -e "$original" ]; then
            echo -e "${RED}Orphaned .meta file: $meta${NC}"
            ORPHANED_META=1
        fi
    done

    if [ $MISSING_META -eq 0 ] && [ $ORPHANED_META -eq 0 ]; then
        echo -e "${GREEN}✓ Project validation passed${NC}"
    else
        echo -e "${RED}✗ Project validation failed${NC}"
        exit 1
    fi
}

# Execute custom Unity method
execute_method() {
    local method=$1
    if [ -z "$method" ]; then
        echo -e "${RED}Usage: execute_method <ClassName.MethodName>${NC}"
        exit 1
    fi

    echo -e "${YELLOW}Executing Unity method: $method${NC}"
    check_unity

    "$UNITY_EDITOR" \
        -quit -batchmode -nographics \
        -projectPath "$PROJECT_PATH" \
        -executeMethod "$method" \
        -logFile "$PROJECT_PATH/execute.log"

    cat "$PROJECT_PATH/execute.log"
}

# Generate Unity meta files for new assets
generate_meta_files() {
    echo -e "${YELLOW}Generating missing .meta files...${NC}"
    check_unity

    "$UNITY_EDITOR" \
        -quit -batchmode -nographics \
        -projectPath "$PROJECT_PATH" \
        -logFile "$PROJECT_PATH/meta-gen.log"

    echo -e "${GREEN}✓ Meta files generated${NC}"
}

# Show help
show_help() {
    cat << EOF
Unity Helper Scripts - Automate Unity operations from command line

Usage: ./unity-helpers.sh [command]

Commands:
    test                Run Unity tests in batch mode
    build-ios           Build project for iOS
    build-android       Build project for Android
    validate            Validate project structure and meta files
    execute <method>    Execute custom Unity static method
    generate-meta       Generate missing .meta files
    help                Show this help message

Examples:
    ./unity-helpers.sh test
    ./unity-helpers.sh build-ios
    ./unity-helpers.sh execute DataImporter.ImportAll
    ./unity-helpers.sh validate

Configuration:
    Edit UNITY_EDITOR and PROJECT_PATH variables at the top of this script
    to match your local setup.

    Current settings:
    - Unity Editor: $UNITY_EDITOR
    - Project Path: $PROJECT_PATH
EOF
}

# Main command dispatcher
case "$1" in
    test)
        run_tests
        ;;
    build-ios)
        build_ios
        ;;
    build-android)
        build_android
        ;;
    validate)
        validate_project
        ;;
    execute)
        execute_method "$2"
        ;;
    generate-meta)
        generate_meta_files
        ;;
    help|--help|-h|"")
        show_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo "Run './unity-helpers.sh help' for usage information"
        exit 1
        ;;
esac
