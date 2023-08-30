def generate_gunicorn_script(output_path, project_path, project_name):
    # Gunicorn启动脚本模板内容
    gunicorn_template = """
#!/bin/bash

NAME="{project_name}"
PROJECT_PATH="{project_path}/{project_name}"
SOCKFILE="{project_path}/{project_name}/{project_name}.sock"
NUM_WORKERS=3

echo "Starting $NAME as `whoami`"

cd $PROJECT_PATH

# 检查FastAPI是否已经在运行
if pgrep -f "gunicorn {project_name}.main:app"; then
    echo "FastAPI service is already running."
    exit 1
else
    echo "Starting FastAPI service..."
    exec gunicorn {project_name}.main:app --worker-class uvicorn.workers.UvicornWorker \
    --bind=unix:$SOCKFILE \
    --workers $NUM_WORKERS \
    --name $NAME \
    --log-level=debug \
    --log-file=- &
    echo "FastAPI service started."
fi
"""
    content = gunicorn_template.format(
        project_path=project_path, project_name=project_name)

    with open(output_path, 'w') as output:
        output.write(content)


def generate_nginx_conf(output_path, project_path, project_name):
    # Nginx配置模板内容
    nginx_template = """
server {{
    listen 6604;
    #server_name your_server_ip;
    access_log  /usr/local/nginx/logs/{project_name}6604.log;
    error_log /usr/local/nginx/logs/{project_name}6604_error.log debug;

    location / {{
        proxy_pass http://unix:{project_path}/{project_name}/{project_name}.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }}

    location /static/ {{
        alias {project_path}/{project_name}/static_assets/;
    }}
}}
"""
    content = nginx_template.format(
        project_path=project_path, project_name=project_name)

    with open(output_path, 'w') as output:
        output.write(content)


if __name__ == "__main__":
    GUNICORN_OUTPUT_PATH = 'gunicorn_start.sh'
    NGINX_OUTPUT_PATH = 'nginx_gunicorn.conf'
    PROJECT_PATH = '/home/pyapp/workspace/env_FastAPI'
    PROJECT_NAME = 'fastapi_project'

    generate_gunicorn_script(GUNICORN_OUTPUT_PATH, PROJECT_PATH, PROJECT_NAME)
    generate_nginx_conf(NGINX_OUTPUT_PATH, PROJECT_PATH, PROJECT_NAME)

