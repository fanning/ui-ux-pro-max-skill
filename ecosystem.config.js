module.exports = {
  apps: [{
    name: 'ui-ux-pro-max',
    script: 'venv/bin/uvicorn',
    args: 'api.web_server:app --host 127.0.0.1 --port 9056',
    cwd: '/home/fanning/ui-ux-pro-max',
    interpreter: 'none',
    max_memory_restart: '150M',
    max_restarts: 10,
    restart_delay: 4000,
    env: {
      PORT: 9056,
      UV_THREADPOOL_SIZE: '2'
    }
  }]
};
