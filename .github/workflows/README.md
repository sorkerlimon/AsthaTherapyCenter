# GitHub Actions Deployment Guide

This repository uses GitHub Actions for automated deployment to the production server using rsync.

## Setup Requirements

### 1. GitHub Secrets Configuration

You need to configure the following secrets in your GitHub repository settings:

#### Server Connection
- `HOST`: Your server IP address or domain (e.g., `123.456.789.0` or `server.example.com`)
- `SSH_USER`: Server username (e.g., `ubuntu`)
- `SSH_PRIVATE_KEY`: Private SSH key for server access
- `SSH_PORT`: SSH port (default: `22`)
- `DEPLOY_PATH`: Deployment path on server (e.g., `/home/ubuntu/asthatherapycenter.com`)

#### Database Configuration
- `DB_HOST`: Database host (e.g., `localhost` or `192.168.0.103`)
- `DB_NAME`: Database name (e.g., `astha_therapy`)
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_PORT`: Database port (default: `3306`)

#### Django Configuration
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Comma-separated allowed hosts (e.g., `asthatherapycenter.com,www.asthatherapycenter.com`)
- `SITE_NAME`: Site name (e.g., `Aastha Therapy Center`)
- `SITE_DOMAIN`: Primary domain (e.g., `asthatherapycenter.com`)

#### Email Configuration (Optional)
- `EMAIL_HOST`: SMTP host (e.g., `smtp.gmail.com`)
- `EMAIL_PORT`: SMTP port (e.g., `587`)
- `EMAIL_USE_TLS`: Use TLS (e.g., `True`)
- `EMAIL_HOST_USER`: Email username
- `EMAIL_HOST_PASSWORD`: Email password/app password

### 2. Server Setup

Ensure your server has the following:

1. **Virtual Environment**: Python virtual environment at `{DEPLOY_PATH}/env/`
2. **System Service**: Systemd service named `asthatherapycenter`
3. **Web Server**: Nginx configured for the domain
4. **Database**: MySQL server with configured database and user
5. **SSL Certificate**: Let's Encrypt or other SSL certificate configured

### 3. SSH Key Setup

1. Generate SSH key pair:
   ```bash
   ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
   ```

2. Add public key to server's `~/.ssh/authorized_keys`

3. Add private key to GitHub secrets as `SSH_PRIVATE_KEY`

### 4. Branch Configuration

The workflow triggers on pushes to the `production` branch. To deploy:

1. Merge your changes to the `production` branch
2. Push to GitHub
3. Monitor the deployment in the Actions tab

### 5. Manual Deployment

You can also trigger deployment manually from the GitHub Actions tab using the "workflow_dispatch" option.

## Deployment Process

The deployment workflow performs the following steps:

1. **Code Checkout**: Downloads the latest code from the production branch
2. **Dependencies**: Installs Python dependencies and runs Django checks
3. **Static Files**: Collects static files for deployment
4. **File Sync**: Uses rsync to sync files to the server (excluding unnecessary files)
5. **Server Commands**: Runs migrations, collects static files, and restarts services
6. **Health Check**: Verifies the site is responding
7. **Status Notification**: Reports deployment success or failure

## Excluded Files

The following files/directories are excluded from deployment:
- `.git/` - Git repository files
- `__pycache__/` - Python cache files
- `*.pyc` - Python compiled files
- `.env.example` - Environment template
- `env_template.txt` - Environment template
- `env/` - Virtual environment (managed separately on server)
- `.gitignore` - Git ignore file
- `README.md` - Documentation
- `db.sqlite3` - SQLite database (production uses MySQL)
- `.github/` - GitHub workflows
- `Deploymnet/` - Deployment notes

## Troubleshooting

### Common Issues

1. **SSH Connection Failed**
   - Verify SSH key is correct
   - Check server SSH configuration
   - Ensure SSH port is correct

2. **Permission Denied**
   - Verify SSH key has proper permissions (600)
   - Check server user permissions
   - Ensure deploy path exists and is writable

3. **Service Restart Failed**
   - Check systemd service configuration
   - Verify service name matches (`asthatherapycenter`)
   - Check server logs: `sudo journalctl -u asthatherapycenter`

4. **Database Connection Failed**
   - Verify database credentials
   - Check database server is running
   - Ensure database and user exist

5. **Static Files Not Loading**
   - Check Nginx configuration
   - Verify static files path
   - Ensure proper permissions on static files

### Manual Server Commands

If deployment fails, you can manually run these commands on the server:

```bash
cd /home/ubuntu/asthatherapycenter.com
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart asthatherapycenter
sudo systemctl restart nginx
```

## Security Considerations

1. **Never commit secrets**: All sensitive data is stored in GitHub secrets
2. **SSH Key Security**: Private keys are never exposed in logs
3. **Environment Variables**: Production environment variables are properly configured
4. **File Permissions**: Proper file permissions are set during deployment
5. **HTTPS Only**: Production site should use HTTPS with valid SSL certificate

## Monitoring

After deployment, monitor:
- Application logs: `sudo journalctl -u asthatherapycenter -f`
- Nginx logs: `sudo tail -f /var/log/nginx/error.log`
- System resources: `htop` or `top`
- Service status: `sudo systemctl status asthatherapycenter nginx`