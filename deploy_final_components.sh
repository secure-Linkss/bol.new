#!/bin/bash

# --- Final Component Mapping Script ---
# This script replaces the old, broken components with the new, verified ones.

echo "Starting final component mapping..."

# 1. Layout Component (RBAC Fix)
echo "Mapping Layout_RoleBased.jsx to Layout.jsx..."
cp src/components/Layout_RoleBased.jsx src/components/Layout.jsx

# 2. Settings Component (Payment Forms & Consolidation Fix)
echo "Mapping Settings_Final.jsx to Settings.jsx..."
cp src/components/Settings_Final.jsx src/components/Settings.jsx

# 3. Admin Panel Component (Comprehensive Tables Fix)
echo "Mapping AdminPanel_WithTables.jsx to AdminPanelComplete.jsx..."
cp src/components/AdminPanel_WithTables.jsx src/components/AdminPanelComplete.jsx

# 4. Tracking Links Component (Data Accuracy Fix)
echo "Mapping TrackingLinks_Final.jsx to TrackingLinks.jsx..."
cp src/components/TrackingLinks_Final.jsx src/components/TrackingLinks.jsx

# 5. Vercel Configuration (404 Reload Fix)
echo "Mapping fixed vercel.json..."
# The vercel.json file was fixed in place, so we just ensure it's staged.

echo "Mapping complete. All files are ready for commit."

# Clean up temporary files
rm src/components/*Final.jsx
rm src/components/*RoleBased.jsx
rm src/components/*WithTables.jsx

echo "Cleanup complete. Ready for local testing and final push."
