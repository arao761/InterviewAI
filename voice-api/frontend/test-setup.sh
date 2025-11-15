#!/bin/bash
# Quick test script for Phase 2 setup

echo "🧪 Testing Phase 2 Setup"
echo "========================"
echo ""

# Check Node.js
echo "1. Checking Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "   ✅ Node.js installed: $NODE_VERSION"
else
    echo "   ❌ Node.js not found"
    exit 1
fi

# Check npm
echo "2. Checking npm..."
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo "   ✅ npm installed: $NPM_VERSION"
else
    echo "   ❌ npm not found"
    exit 1
fi

# Check dependencies
echo "3. Checking dependencies..."
if [ -d "node_modules" ]; then
    echo "   ✅ Dependencies installed"
else
    echo "   ⚠️  Dependencies not installed"
    echo "   Run: npm install"
    exit 1
fi

# Check TypeScript
echo "4. Checking TypeScript..."
if [ -f "node_modules/.bin/tsc" ]; then
    echo "   ✅ TypeScript available"
else
    echo "   ❌ TypeScript not found"
    exit 1
fi

# Check source files
echo "5. Checking source files..."
REQUIRED_FILES=(
    "src/audio-recorder.ts"
    "src/audio-recorder-config.ts"
    "src/api-client.ts"
    "src/demo.ts"
    "public/index.html"
)

ALL_FILES_EXIST=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file missing"
        ALL_FILES_EXIST=false
    fi
done

if [ "$ALL_FILES_EXIST" = false ]; then
    exit 1
fi

# Type check
echo "6. Running TypeScript type check..."
if npm run type-check &> /dev/null; then
    echo "   ✅ TypeScript compilation successful"
else
    echo "   ⚠️  TypeScript errors found (check output above)"
fi

echo ""
echo "✅ Setup check complete!"
echo ""
echo "Next steps:"
echo "  1. Start dev server: npm run dev"
echo "  2. Open http://localhost:3000 in your browser"
echo "  3. Test recording functionality"
echo ""

