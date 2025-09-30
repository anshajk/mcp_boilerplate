# MCP Boilerplate

This repository contains the code to demonstrate MCP capabilities

## Setup instructions 

1. Install python. The repository assumes you have `python 3.12` installed and available on your system. To check write `python3 --version` on your terminal
2. Create a virtual environment and setup dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate 
pip install -r requirements.txt
```


## To deploy Remote MCP

We're going to deploy a remote MCP server to google cloud which also supports authentication. Navigate to the server `remote-mcp-gcp` directory and perform the following steps

1. Install [uv](https://docs.astral.sh/uv/) on your computer if you'd like to run the invoke the MCP server locally using your testing script.
2. Rename `.envrc_sample` to .envrc so that your shell can pickup the GCLOUD_PROJECT_ID environment variable `mv .envrc_sample .envrc` 
3. Update your GCLOUD_PROJECT_ID in your `.envrc` file with the ID of your google cloud project. 
4. Create a container registry to host your MCP server container image

```bash
 gcloud artifacts repositories create remote-mcp-servers \
  --repository-format=docker \
  --location=us-central1 \
  --description="Repository for remote MCP servers" \
  --project=$GCLOUD_PROJECT_ID
  ```

5. Submit a build job for the container image. We'll use remote build for this. 
```bash
gcloud builds submit --region=us-central1 --tag us-central1-docker.pkg.dev/$GCLOUD_PROJECT_ID/remote-mcp-servers/mcp-server:latest
```
6. Create a container cloud run instance with 
```bash
gcloud run deploy mcp-server \
  --image us-central1-docker.pkg.dev/$GCLOUD_PROJECT_ID/remote-mcp-servers/mcp-server:latest \
  --region=us-central1 \
  --no-allow-unauthenticated
  ```
7. Create a proxy to invoke the remote endpoint from your computer with authentication. `gcloud run services proxy mcp-server --region=us-central1`. This will ask you to install cloud run proxy tooling on your computer. 
8. Now, `localhost:8080` should be pointed to your deployed instance with authentication enabled
9. Run `uv run test_server.py` to invoke the client script against the remote server with various tools.

Feel free to create new tools and experiment. 

> [!IMPORTANT]
> Once you're done, delete all associated resources from Google Cloud to avoid unnecessary charges.

## FAQ

1. FastMCP vs MCP Python SDK.[Read this issue for more info](https://github.com/modelcontextprotocol/python-sdk/issues/1068) but generally FastMCP is much more preferred by developers and you'll be able to build much more capabilties with the same. 

