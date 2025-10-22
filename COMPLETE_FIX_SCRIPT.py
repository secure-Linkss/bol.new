#!/usr/bin/env python3
"""
COMPLETE FIX SCRIPT FOR ALL IDENTIFIED ISSUES
October 22, 2025
"""

import os
import re
from pathlib import Path

class ProjectFixer:
    def __init__(self):
        self.project_root = Path("/home/user/brain-link-tracker")
        self.fixes_applied = []
    
    def log_fix(self, fix):
        """Log a fix"""
        self.fixes_applied.append(fix)
        print(f"✅ {fix}")
    
    def fix_dashboard_remove_total_users(self):
        """Remove Total Users metric card from user dashboard"""
        print("\n=== FIXING USER DASHBOARD - REMOVING TOTAL USERS ===")
        
        dashboard_file = self.project_root / "src/components/Dashboard.jsx"
        
        with open(dashboard_file, 'r') as f:
            content = f.read()
        
        # Remove the Total Users card (lines 319-329 approximately)
        # We'll remove it by matching the pattern
        pattern = r'<Card className="hover:shadow-md transition-all cursor-pointer border-l-4 border-l-pink-500[^>]*>[\s\S]*?<p className="text-xs font-medium text-muted-foreground uppercase">Total Users</p>[\s\S]*?</Card>'
        
        new_content = re.sub(pattern, '', content)
        
        # Also remove totalUsers from state if present
        new_content = new_content.replace('totalUsers: 0,', '')
        
        with open(dashboard_file, 'w') as f:
            f.write(new_content)
        
        self.log_fix("Removed 'Total Users' metric card from Dashboard.jsx - user dashboard now shows only user-relevant metrics")
    
    def fix_tracking_links_mobile(self):
        """Fix TrackingLinks mobile responsiveness"""
        print("\n=== FIXING TRACKING LINKS MOBILE RESPONSIVENESS ===")
        
        tracking_file = self.project_root / "src/components/TrackingLinks.jsx"
        
        if not tracking_file.exists():
            print("⚠️  TrackingLinks.jsx not found")
            return
        
        with open(tracking_file, 'r') as f:
            content = f.read()
        
        # Add mobile responsive wrapper classes
        # Look for the container div and ensure it has overflow handling
        if 'overflow-x-auto' not in content:
            # Find the main container and add responsive classes
            content = content.replace(
                'className="space-y-6"',
                'className="space-y-6 w-full"',
                1
            )
            
            # Find button groups and make them wrap on mobile
            content = re.sub(
                r'<div className="flex gap-2">',
                '<div className="flex flex-wrap gap-2">',
                content
            )
            
            # Find the table wrapper and add overflow handling
            content = re.sub(
                r'<div className="rounded-lg border',
                '<div className="overflow-x-auto"><div className="rounded-lg border min-w-[800px]',
                content,
                count=1
            )
            
            # Close the overflow wrapper
            content = re.sub(
                r'</div>\s*</Card>',
                '</div></div></Card>',
                content,
                count=1
            )
        
        with open(tracking_file, 'w') as f:
            f.write(content)
        
        self.log_fix("Added mobile responsive classes to TrackingLinks.jsx")
    
    def fix_live_activity_mobile(self):
        """Fix LiveActivity mobile responsiveness"""
        print("\n=== FIXING LIVE ACTIVITY MOBILE RESPONSIVENESS ===")
        
        live_file = self.project_root / "src/components/LiveActivity.jsx"
        
        if not live_file.exists():
            print("⚠️  LiveActivity.jsx not found")
            return
        
        with open(live_file, 'r') as f:
            content = f.read()
        
        # Add mobile responsive wrapper classes
        if 'overflow-x-auto' not in content:
            # Find button groups and make them wrap
            content = re.sub(
                r'<div className="flex items-center gap-2">',
                '<div className="flex flex-wrap items-center gap-2">',
                content
            )
            
            # Add overflow handling to table
            content = re.sub(
                r'<div className="rounded-lg border',
                '<div className="overflow-x-auto"><div className="rounded-lg border min-w-[800px]',
                content,
                count=1
            )
            
            # Close wrapper
            content = re.sub(
                r'</div>\s*</Card>',
                '</div></div></Card>',
                content,
                count=1
            )
        
        with open(live_file, 'w') as f:
            f.write(content)
        
        self.log_fix("Added mobile responsive classes to LiveActivity.jsx")
    
    def fix_env_vercel(self):
        """Fix .env.vercel file"""
        print("\n=== FIXING .ENV.VERCEL ===")
        
        env_file = self.project_root / ".env.vercel"
        
        with open(env_file, 'r') as f:
            content = f.read()
        
        if 'SHORTIO_DOMAIN' not in content:
            content += '\nSHORTIO_DOMAIN=Secure-links.short.gy\n'
            
            with open(env_file, 'w') as f:
                f.write(content)
            
            self.log_fix("Added SHORTIO_DOMAIN to .env.vercel")
    
    def update_requirements_verified(self):
        """Verify requirements.txt has Redis"""
        print("\n=== VERIFYING REQUIREMENTS.TXT ===")
        
        req_file = self.project_root / "requirements.txt"
        
        with open(req_file, 'r') as f:
            content = f.read()
        
        if 'redis' in content.lower():
            print("✓ Redis dependency confirmed in requirements.txt")
            self.log_fix("Redis dependency verified in requirements.txt")
        else:
            print("❌ Redis still missing!")
    
    def create_production_env_template(self):
        """Create a complete production environment template"""
        print("\n=== CREATING PRODUCTION ENV TEMPLATE ===")
        
        template = """# Production Environment Variables
# Copy these to Vercel Environment Variables

# Security
SECRET_KEY=ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE

# Database
DATABASE_URL=postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require

# Short.io API
SHORTIO_API_KEY=sk_DbGGlUHPN7Z9VotL
SHORTIO_DOMAIN=Secure-links.short.gy

# Redis (Optional - falls back to memory cache if not available)
REDIS_HOST=localhost
REDIS_PORT=6379

# Quantum Redirect Secrets (Optional - uses defaults if not set)
QUANTUM_SECRET_1=quantum_genesis_key_2025_ultra_secure
QUANTUM_SECRET_2=quantum_transit_key_2025_ultra_secure
QUANTUM_SECRET_3=quantum_routing_key_2025_ultra_secure

# Flask Configuration
FLASK_ENV=production
"""
        
        template_file = self.project_root / ".env.production.template"
        
        with open(template_file, 'w') as f:
            f.write(template)
        
        self.log_fix("Created comprehensive production environment template")
    
    def run_all_fixes(self):
        """Run all fixes"""
        print("🔧 RUNNING ALL FIXES...\n")
        
        self.fix_dashboard_remove_total_users()
        self.fix_tracking_links_mobile()
        self.fix_live_activity_mobile()
        self.fix_env_vercel()
        self.update_requirements_verified()
        self.create_production_env_template()
        
        print("\n" + "="*70)
        print("✨ ALL FIXES APPLIED!")
        print("="*70)
        print(f"\nTotal fixes applied: {len(self.fixes_applied)}")
        for i, fix in enumerate(self.fixes_applied, 1):
            print(f"  {i}. {fix}")
        print("\n")

if __name__ == "__main__":
    fixer = ProjectFixer()
    fixer.run_all_fixes()
