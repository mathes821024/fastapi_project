def generate_uvicorn_script(output_path, project_path, project_name):
    # Uvicorn启动脚本模板内容
    uvicorn_template = """
#!/bin/bash

cd {project_path}/{project_name}

# 检查FastAPI是否已经在运行
if pgrep -f "uvicorn {project_name}.main:app"; then
    echo "FastAPI service is already running."
    exit 1
else
    echo "Starting FastAPI service..."
    uvicorn {project_name}.main:app --workers 4 >> fastapi.log 2>&1 &
    echo "FastAPI service started."
fi
"""
    content = uvicorn_template.format(project_path=project_path, project_name=project_name)

    with open(output_path, 'w') as output:
        output.write(content)

if __name__ == "__main__":
    UVICORN_OUTPUT_PATH = 'start_fastapi.sh'
    PROJECT_PATH = '/home/pyapp/workspace/env_FastAPI'
    PROJECT_NAME = 'fastapiMyToolWeb'

    generate_uvicorn_script(UVICORN_OUTPUT_PATH, PROJECT_PATH, PROJECT_NAME)
