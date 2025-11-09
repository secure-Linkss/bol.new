#!/usr/bin/env python3
"""
Comprehensive Frontend Diagnostic Script
Identify all issues causing the white screen on Vercel
"""

import os
import json
import subprocess
import sys

class FrontendDiagnostic:
    def __init__(self):
        self.issues = []
        self.warnings = []
        
    def log_issue(self, issue):
        self.issues.append(issue)
        print(f"❌ ISSUE: {issue}")
        
    def log_warning(self, warning):
        self.warnings.append(warning)
        print(f"⚠️  WARNING: {warning}")
        
    def log_success(self, message):
        print(f"✅ {message}")
    
    def check_package_json(self):
        """Check package.json for issues"""
        print("\n🔍 Checking package.json...")
        
        if not os.path.exists('package.json'):
            self.log_issue("package.json not found")
            return False
            
        try:
            with open('package.json', 'r') as f:
                pkg = json.load(f)
            
            # Check required scripts
            scripts = pkg.get('scripts', {})
            required_scripts = ['build', 'dev']
            for script in required_scripts:
                if script not in scripts:
                    self.log_issue(f"Missing script: {script}")
                else:
                    self.log_success(f"Script found: {script}")
            
            # Check dependencies
            deps = pkg.get('dependencies', {})
            critical_deps = ['react', 'react-dom', 'react-router-dom']
            for dep in critical_deps:
                if dep not in deps:
                    self.log_issue(f"Missing critical dependency: {dep}")
                else:
                    self.log_success(f"Dependency found: {dep}")
            
            return True
            
        except Exception as e:
            self.log_issue(f"Error parsing package.json: {str(e)}")
            return False
    
    def check_index_html(self):
        """Check index.html"""
        print("\n🔍 Checking index.html...")
        
        if not os.path.exists('index.html'):
            self.log_issue("index.html not found in root")
            
        # Check in public directory
        if os.path.exists('public/index.html'):
            self.log_success("index.html found in public directory")
        else:
            self.log_warning("index.html not found in public directory")
            
        # Check dist directory after build
        if os.path.exists('dist/index.html'):
            self.log_success("index.html found in dist directory")
            
            # Check content
            try:
                with open('dist/index.html', 'r') as f:
                    content = f.read()
                    
                if 'root' in content:
                    self.log_success("Root div found in index.html")
                else:
                    self.log_issue("Root div not found in index.html")
                    
                if 'script' in content:
                    self.log_success("Script tags found in index.html")
                else:
                    self.log_issue("No script tags found in index.html")
                    
            except Exception as e:
                self.log_issue(f"Error reading dist/index.html: {str(e)}")
        else:
            self.log_warning("dist/index.html not found - need to build first")
    
    def check_main_files(self):
        """Check main application files"""
        print("\n🔍 Checking main application files...")
        
        main_files = [
            'src/App.jsx',
            'src/main.jsx',
            'src/index.js',  # Alternative
            'src/components/Layout.jsx'
        ]
        
        for file_path in main_files:
            if os.path.exists(file_path):
                self.log_success(f"Found: {file_path}")
                
                # Check for syntax errors
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        
                    # Basic syntax checks
                    if 'import React' in content or 'import { ' in content:
                        self.log_success(f"{file_path}: Import statements look good")
                    
                    if 'export default' in content:
                        self.log_success(f"{file_path}: Default export found")
                    
                except Exception as e:
                    self.log_issue(f"Error reading {file_path}: {str(e)}")
            else:
                if file_path in ['src/main.jsx', 'src/index.js']:
                    self.log_warning(f"Optional file not found: {file_path}")
                else:
                    self.log_issue(f"Required file not found: {file_path}")
    
    def check_vite_config(self):
        """Check Vite configuration"""
        print("\n🔍 Checking Vite configuration...")
        
        if os.path.exists('vite.config.js'):
            self.log_success("vite.config.js found")
            
            try:
                with open('vite.config.js', 'r') as f:
                    content = f.read()
                    
                if '@vitejs/plugin-react' in content:
                    self.log_success("React plugin configured")
                else:
                    self.log_issue("React plugin not found in vite.config.js")
                    
            except Exception as e:
                self.log_issue(f"Error reading vite.config.js: {str(e)}")
        else:
            self.log_issue("vite.config.js not found")
    
    def check_environment_variables(self):
        """Check environment variables"""
        print("\n🔍 Checking environment variables...")
        
        env_files = ['.env', '.env.local', '.env.production', '.env.vercel']
        
        for env_file in env_files:
            if os.path.exists(env_file):
                self.log_success(f"Found: {env_file}")
            else:
                self.log_warning(f"Not found: {env_file}")
    
    def check_build_output(self):
        """Check build output"""
        print("\n🔍 Checking build output...")
        
        if os.path.exists('dist'):
            files = os.listdir('dist')
            self.log_success(f"dist directory contains {len(files)} files")
            
            # Check for critical files
            critical_files = ['index.html', 'assets']
            for file in critical_files:
                if file in files:
                    self.log_success(f"Found in dist: {file}")
                else:
                    self.log_issue(f"Missing from dist: {file}")
                    
            # Check assets directory
            if os.path.exists('dist/assets'):
                assets = os.listdir('dist/assets')
                js_files = [f for f in assets if f.endswith('.js')]
                css_files = [f for f in assets if f.endswith('.css')]
                
                self.log_success(f"Assets: {len(js_files)} JS files, {len(css_files)} CSS files")
                
                if not js_files:
                    self.log_issue("No JavaScript files found in dist/assets")
                if not css_files:
                    self.log_warning("No CSS files found in dist/assets")
            
        else:
            self.log_issue("dist directory not found - build required")
    
    def check_import_paths(self):
        """Check for import path issues"""
        print("\n🔍 Checking import paths...")
        
        # Check if components can be imported
        component_files = []
        if os.path.exists('src/components'):
            for root, dirs, files in os.walk('src/components'):
                for file in files:
                    if file.endswith('.jsx') or file.endswith('.js'):
                        component_files.append(os.path.join(root, file))
        
        self.log_success(f"Found {len(component_files)} component files")
        
        # Check for common import issues
        import_issues = 0
        for file_path in component_files[:10]:  # Check first 10 files
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Check for absolute imports that might fail
                if 'import.*@/' in content and '@' not in content:
                    import_issues += 1
                    
            except Exception as e:
                self.log_warning(f"Could not check imports in {file_path}: {str(e)}")
        
        if import_issues > 0:
            self.log_warning(f"Found {import_issues} files with potential import issues")
    
    def test_build(self):
        """Test if build works"""
        print("\n🔍 Testing build process...")
        
        try:
            result = subprocess.run(['npm', 'run', 'build'], 
                                  capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                self.log_success("Build completed successfully")
                return True
            else:
                self.log_issue(f"Build failed with error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log_issue("Build timed out after 2 minutes")
            return False
        except Exception as e:
            self.log_issue(f"Error running build: {str(e)}")
            return False
    
    def run_comprehensive_check(self):
        """Run all diagnostic checks"""
        print("🚀 Frontend Comprehensive Diagnostic")
        print("=" * 60)
        
        checks = [
            self.check_package_json,
            self.check_vite_config,
            self.check_main_files,
            self.check_environment_variables,
            self.check_import_paths,
            self.test_build,
            self.check_build_output,
            self.check_index_html
        ]
        
        for check in checks:
            try:
                check()
            except Exception as e:
                self.log_issue(f"Diagnostic check failed: {str(e)}")
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 DIAGNOSTIC SUMMARY")
        print("=" * 60)
        
        print(f"❌ Issues Found: {len(self.issues)}")
        for issue in self.issues:
            print(f"   - {issue}")
        
        print(f"\n⚠️  Warnings: {len(self.warnings)}")
        for warning in self.warnings:
            print(f"   - {warning}")
        
        if len(self.issues) == 0:
            print("\n🎉 No critical issues found!")
            return True
        else:
            print(f"\n🔧 Found {len(self.issues)} issues that need fixing")
            return False

if __name__ == "__main__":
    diagnostic = FrontendDiagnostic()
    success = diagnostic.run_comprehensive_check()
    sys.exit(0 if success else 1)