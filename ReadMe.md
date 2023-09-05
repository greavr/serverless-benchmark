# Storage Load Testing
This application is designed to run inside a docker container and performance test different backends:
- CloudSQL
  - Public IP
  - Private IP
  - Cloud SQL Proxy
- GCS Fuse
- Filestore (NFS)
- Local Storage

## Run Code Locally
```python
cd code
pip3 install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r src/requirements.txt
export GCP_PROJECT=$(gcloud config get-value project)
```

**Deactivate the environment** 
Run the following command
```
deactivate
```

## Environment Variables ##
The following environment variables can be set:
  - **ENABLE_LOGGING** - BOOL - Enable Logging
  - **ENABLE_APM** - BOOL - Enable APM
  - **NFS_VOLUME** - STR - Mount path to NFS Volume
  - **GCS_FUSE_VOLUME** - STR - Path to GCS fuse
  
# Org Policy:
- **iam.allowedPolicyMemberDomains** - Set to***All***