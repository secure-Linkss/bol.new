#!/usr/bin/env python3
import os
import sys
import ast
import traceback
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 80)
print("COMPREHENSIVE PROJECT ANALYSIS - BRAIN LINK TRACKER")
print("=" * 80)

def analyze_python_syntax(file_path):
    """Analyze Python file for syntax errors"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to parse the AST
        ast.parse(content)
        return True, None
    except SyntaxError as e:
        return False, f"Syntax Error: {e.msg} at line {e.lineno}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def analyze_imports(file_path):
    """Analyze imports in Python file"""
    issues = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse AST to find imports
        tree = ast.parse(content)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # Check if it's a relative import that might fail
                    if alias.name.startswith('.'):
                        issues.append(f"Relative import: {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith('.'):
                    issues.append(f"Relative import: from {node.module} import ...")
                    
    except Exception as e:
        issues.append(f"Failed to analyze imports: {str(e)}")
    
    return issues

print("\n1. PYTHON SYNTAX ANALYSIS")
print("-" * 40)

python_files = []
for root, dirs, files in os.walk('.'):
    # Skip git and node_modules directories
    dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.pytest_cache']]
    
    for file in files:
        if file.endswith('.py'):
            python_files.append(os.path.join(root, file))

syntax_errors = []
import_issues = []

for py_file in python_files:
    is_valid, error = analyze_python_syntax(py_file)
    if not is_valid:
        syntax_errors.append((py_file, error))
        print(f"❌ {py_file}: {error}")
    else:
        print(f"✅ {py_file}: Syntax OK")
        
        # Analyze imports
        imports = analyze_imports(py_file)
        if imports:
            import_issues.extend([(py_file, issue) for issue in imports])

print(f"\nSyntax Summary: {len(syntax_errors)} errors found in {len(python_files)} Python files")

if import_issues:
    print(f"\nImport Issues: {len(import_issues)} potential issues")
    for file, issue in import_issues:
        print(f"  - {file}: {issue}")

print("\n2. DATABASE SCHEMA ANALYSIS")
print("-" * 40)

try:
    import psycopg2
    
    database_url = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name;
    """)
    tables = [table[0] for table in cursor.fetchall()]
    
    # Identify duplicate table issues
    potential_duplicates = []
    if 'user' in tables and 'users' in tables:
        potential_duplicates.append(('user', 'users'))
    if 'link' in tables and 'links' in tables:
        potential_duplicates.append(('link', 'links'))
    if 'campaign' in tables and 'campaigns' in tables:
        potential_duplicates.append(('campaign', 'campaigns'))
    if 'tracking_event' in tables and 'tracking_events' in tables:
        potential_duplicates.append(('tracking_event', 'tracking_events'))
    if 'notification' in tables and 'notifications' in tables:
        potential_duplicates.append(('notification', 'notifications'))
    
    if potential_duplicates:
        print("❌ DUPLICATE TABLE ISSUES FOUND:")
        for old_table, new_table in potential_duplicates:
            print(f"  - Duplicate tables: {old_table} and {new_table}")
            
            # Check data in both tables
            cursor.execute(f"SELECT COUNT(*) FROM {old_table};")
            old_count = cursor.fetchone()[0]
            cursor.execute(f"SELECT COUNT(*) FROM {new_table};")
            new_count = cursor.fetchone()[0]
            
            print(f"    {old_table}: {old_count} records")
            print(f"    {new_table}: {new_count} records")
    else:
        print("✅ No duplicate table issues found")
    
    # Check foreign key constraints
    cursor.execute("""
        SELECT DISTINCT
            tc.table_name,
            kcu.column_name,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name,
            tc.constraint_name
        FROM 
            information_schema.table_constraints AS tc 
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
              AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
              AND ccu.table_schema = tc.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY';
    """)
    foreign_keys = cursor.fetchall()
    
    print(f"\n✅ Foreign Key Analysis: {len(foreign_keys)} constraints found")
    
    # Check for broken foreign keys
    fk_issues = []
    for fk in foreign_keys:
        table_name, column_name, foreign_table, foreign_column, constraint_name = fk
        
        # Check if referenced table exists
        if foreign_table not in tables:
            fk_issues.append(f"Table {table_name}.{column_name} references non-existent table {foreign_table}")
    
    if fk_issues:
        print("❌ FOREIGN KEY ISSUES:")
        for issue in fk_issues:
            print(f"  - {issue}")
    else:
        print("✅ All foreign key references are valid")
    
    cursor.close()
    conn.close()

except Exception as e:
    print(f"❌ Database analysis failed: {str(e)}")
    traceback.print_exc()

print("\n3. MODEL DEFINITION ANALYSIS")
print("-" * 40)

# Check models directory
models_dir = Path("src/models")
if models_dir.exists():
    model_files = list(models_dir.glob("*.py"))
    print(f"Found {len(model_files)} model files:")
    
    for model_file in model_files:
        if model_file.name != "__init__.py":
            print(f"  - {model_file}")
            
            # Check for table name definitions
            try:
                with open(model_file, 'r') as f:
                    content = f.read()
                    
                if "__tablename__" in content:
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if "__tablename__" in line:
                            print(f"    Table: {line.strip()}")
                            
            except Exception as e:
                print(f"    Error reading {model_file}: {e}")
else:
    print("❌ Models directory not found")

print("\n4. ROUTE ANALYSIS")
print("-" * 40)

routes_dir = Path("src/routes")
if routes_dir.exists():
    route_files = list(routes_dir.glob("*.py"))
    print(f"Found {len(route_files)} route files:")
    
    for route_file in route_files:
        if route_file.name != "__init__.py":
            print(f"  - {route_file}")
else:
    print("❌ Routes directory not found")

print("\n5. VERCEL COMPATIBILITY CHECK")
print("-" * 40)

# Check Python version compatibility
import sys
python_version = sys.version_info
print(f"Current Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")

if python_version.major == 3 and python_version.minor >= 9:
    print("✅ Python version is compatible with Vercel")
else:
    print("❌ Python version may not be compatible with Vercel (requires Python 3.9+)")

# Check requirements.txt for Vercel compatibility
print("\nChecking requirements.txt for Vercel compatibility...")
if os.path.exists("requirements.txt"):
    with open("requirements.txt", 'r') as f:
        requirements = f.read()
    
    # Check for problematic packages
    problematic_packages = []
    if "gevent" in requirements:
        problematic_packages.append("gevent (may cause issues on Vercel)")
    if "gunicorn" in requirements:
        print("✅ gunicorn found (good for production)")
    
    if problematic_packages:
        print("⚠️  Potentially problematic packages:")
        for pkg in problematic_packages:
            print(f"  - {pkg}")
    else:
        print("✅ No obviously problematic packages found")
        
# Check vercel.json configuration
if os.path.exists("vercel.json"):
    print("✅ vercel.json found")
    with open("vercel.json", 'r') as f:
        vercel_config = f.read()
    
    if '"@vercel/python"' in vercel_config:
        print("✅ Vercel Python runtime configured")
    else:
        print("❌ Vercel Python runtime not configured")
else:
    print("❌ vercel.json not found")

print("\n6. ENVIRONMENT VARIABLES CHECK")
print("-" * 40)

required_env_vars = ['SECRET_KEY', 'DATABASE_URL', 'SHORTIO_API_KEY', 'SHORTIO_DOMAIN']
missing_vars = []

for var in required_env_vars:
    if os.environ.get(var):
        print(f"✅ {var}: Configured")
    else:
        missing_vars.append(var)
        print(f"❌ {var}: Missing")

if missing_vars:
    print(f"\n❌ Missing environment variables: {', '.join(missing_vars)}")
else:
    print("\n✅ All required environment variables are configured")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)

print(f"\nSUMMARY:")
print(f"- Python files analyzed: {len(python_files)}")
print(f"- Syntax errors: {len(syntax_errors)}")
print(f"- Import issues: {len(import_issues)}")
print(f"- Database tables: {len(tables) if 'tables' in locals() else 'Unknown'}")
print(f"- Duplicate table pairs: {len(potential_duplicates) if 'potential_duplicates' in locals() else 'Unknown'}")
print(f"- Foreign key issues: {len(fk_issues) if 'fk_issues' in locals() else 'Unknown'}")
print(f"- Missing environment variables: {len(missing_vars)}")

if syntax_errors or (potential_duplicates if 'potential_duplicates' in locals() else []) or (fk_issues if 'fk_issues' in locals() else []) or missing_vars:
    print(f"\n❌ Issues found that need to be fixed!")
else:
    print(f"\n✅ No critical issues found!")