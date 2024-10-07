module.exports = {
    apps: [
        {
            name: 'apex-python-cron',
            script: 'uvicorn',
            args: 'main:app --host 127.0.0.1 --port 3000',
            interpreter: '/usr/bin/python3',
            interpreter_args: '-u',
            watch: true,
        },
    ],
};
