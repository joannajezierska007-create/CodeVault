#!/usr/bin/env python3
"""
CodeVault EXE Builder
This script builds the CodeVault EXE executable using PyInstaller.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    print("=" * 60)
    print("CodeVault EXE Builder")
    print("=" * 60)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyInstaller==6.8.1"])
        print("✓ PyInstaller installed successfully")
    
    # Get the repository root
    repo_root = Path(__file__).parent
    spec_file = repo_root / "build_exe.spec"
    
    if not spec_file.exists():
        print(f"✗ build_exe.spec not found at {spec_file}")
        return False
    
    print(f"✓ Found build_exe.spec")
    
    # Clean previous builds
    print("\nCleaning previous builds...")
    build_dir = repo_root / "build"
    dist_dir = repo_root / "dist"
    
    if build_dir.exists():
        shutil.rmtree(build_dir)
        print(f"✓ Removed {build_dir}")
    
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
        print(f"✓ Removed {dist_dir}")
    
    # Build the EXE
    print("\nBuilding CodeVault EXE...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller",
            str(spec_file),
            "--clean"
        ])
        print("✓ Build completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed with error code {e.returncode}")
        return False
    
    # Verify the EXE exists
    exe_path = dist_dir / "CodeVault" / "CodeVault.exe"
    if exe_path.exists():
        exe_size = exe_path.stat().st_size / (1024 * 1024)
        print(f"\n✓ CodeVault.exe created successfully!")
        print(f"  Location: {exe_path}")
        print(f"  Size: {exe_size:.2f} MB")
        print(f"\nYou can now run: {exe_path}")
        return True
    else:
        print(f"✗ CodeVault.exe not found at expected location: {exe_path}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
