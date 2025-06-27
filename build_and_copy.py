import os
import shutil
import subprocess

# Paths
frontend_path = 'frontend'
dist_path = os.path.join(frontend_path, 'dist')
backend_static_path = 'backend/static'  # Adjust if you're using a different static_folder

# Step 1: Build Vue frontend
print("🛠️  Building Vue frontend...")
subprocess.run(['npm', 'run', 'build'], cwd=frontend_path, check=True)

# Step 2: Remove old static files
if os.path.exists(backend_static_path):
    print("🧹 Removing old backend static files...")
    shutil.rmtree(backend_static_path)

# Step 3: Copy new dist files
print("📁 Copying new dist files to backend...")
shutil.copytree(dist_path, backend_static_path)

print("✅ Done! Frontend built and copied to Flask backend.")
