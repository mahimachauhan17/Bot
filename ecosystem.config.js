module.exports = {
  apps: [
    {
      name: 'interviewer-ai-backend',
      cwd: './backend',
      script: 'daphne',
      args: '-b 0.0.0.0 -p 8000 config.asgi:application',
      interpreter: './venv/bin/python',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        DJANGO_SETTINGS_MODULE: 'config.settings',
      },
    },
    {
      name: 'interviewer-ai-celery',
      cwd: './backend',
      script: 'celery',
      args: '-A config worker -l info',
      interpreter: './venv/bin/python',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
    },
    {
      name: 'interviewer-ai-frontend',
      cwd: './frontend',
      script: 'npm',
      args: 'start',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
    },
  ],
}
