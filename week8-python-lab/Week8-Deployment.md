# **Week 8 Python FastAPI Lab – Containerize and Deploy to the Cloud (AWS)**

## **1. Before Class (Individual)**

1. **Register for an AWS Free Tier Account**  
   - Be aware that some AWS services (like ECS) might incur charges once you exceed the free tier.   
2. **Install Docker Desktop**  
   - **Windows**: [Install Docker for Windows](https://docs.docker.com/docker-for-windows/install/). Choose **WSL 2** or **Hyper-V** backend.  
   - **macOS**: [Install Docker for Mac](https://docs.docker.com/docker-for-mac/install/).  
   - Verify Docker is running: follow the [Get Started tutorial](https://docs.docker.com/get-started/).  
3. **Create a Docker Hub Account**  
   - Sign in to Docker Desktop with your Docker Hub credentials to link the account.  

Make sure Docker is properly installed and running on your system before class.

4. **Download the Lab Repository**:
You can use [DownGit](https://downgit.github.io/#/) to download only the specific folder you need from the repository.

- 1. **Open DownGit**  
   Visit [https://downgit.github.io/#/](https://downgit.github.io/#/).

- 2. **Paste the Folder URL**  
   Use the following URL for the `week8-python-lab` folder:
   ```
   https://github.com/chenzhi-cz/IS631-Modern-Software-Development/tree/main/week8-python-lab
   ```

- 3. **Download the Folder**  
   - Paste the URL into the DownGit interface.
   - Click the "Download" button.
   - A `.zip` file containing only the `week8-python-lab` folder will be downloaded.

- 4. **Extract the Folder**  
   Extract the `.zip` file to access the `week8-python-lab` content.

---

## **2. Activity 1 (Individual): Build a Docker Image of Your FastAPI App**

Assuming you have a **Python FastAPI** project from **Week 6**, let’s containerize it.

### **(a) Open Your Week 6 Project**

- Launch VS Code and open project.  

### **(b) Create a `Dockerfile`**

Inside your project folder, create a file named **`Dockerfile`** with contents similar to:

```dockerfile
# Use an official Python base image
FROM python:3.10-slim

# Create a working directory inside the container
WORKDIR /book_app

# Copy your requirements file
COPY requirements.txt /book_app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . /book_app

# Expose port 8000 (FastAPI default)
EXPOSE 8000

# Start FastAPI with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

> **Notes**:  
> - Adjust Python version as needed.  
> - Make sure `requirements.txt` includes all your project dependencies (FastAPI, SQLAlchemy, etc.).  
> - If your entry point file is something other than `main.py`, update the `CMD` line accordingly (e.g., `"app.main:app"`).

### **(c) Build the Docker Image**

From your VS Code **terminal** (in the root of the project), run:

```bash
docker build -t book-app:1.0.0 .
```

- `-t book-app:1.0.0` gives your image a name (`book-app`) and a tag (`1.0.0`).  
- **`.`** means “use the current directory” (which has the Dockerfile).

You should see Docker processing each step. When it finishes, run:

```bash
docker images
```
to confirm your new image (`book-app:1.0.0`) is present.

### **(d) Test the Image Locally**

Launch a container from your newly built image:

```bash
docker run -it -p 8000:8000 book-app:1.0.0
```

- `-p 8000:8000` forwards port 8000 on your **host** to port 8000 inside the container.
- FastAPI should now be accessible at [http://localhost:8000](http://localhost:8000).  
- If you have routes like `/books`, you can access [http://localhost:8000/books](http://localhost:8000/books).

Press **Ctrl+C** to stop the container.  
You can also use:

```bash
docker ps           # list running containers
docker stop <id>    # stop a specific container by its name or ID
```

---

## **3. Activity 2 (Individual): Push the Docker Image to DockerHub**

### **(a) Create a New Public Repository on DockerHub**

- On [Docker Hub](https://hub.docker.com/), create a **public** repository named something like `bookapp`.  
- You’ll push your local image to this repository so anyone can pull it.

### **(b) Tag the Local Image for DockerHub**

Right now, you have `book-app:1.0.0` locally. To push it to DockerHub, it needs a name in the format **`<dockerhub_username>/<repo>:<tag>`**.

Run:

```bash
docker tag book-app:1.0.0 <your_dockerhub_id>/bookapp:1.0
```

- Replace `<your_dockerhub_id>` with your actual Docker Hub username.
- Optionally change `:1.0` to a different tag if you want a version scheme.

### **(c) Push the Image to DockerHub**

```bash
docker push <your_dockerhub_id>/bookapp:1.0
```

Docker will upload your layers to Docker Hub. Once the upload is complete, navigate to the Docker Hub interface and locate your image in the `bookapp` repository. Click on the `Tags` tab to view the image details. Take note of the `OS/ARCH` of the image, which might be `linux/arm64` or `linux/x86_64`. This information is important, as you'll need to select the same `OS/ARCH` when deploying the image to AWS services.

---

## **4. Activity 3: Set Up CI and Deploy to AWS**

Below is **Activity 3** for deploying your FastAPI **book-app** Docker image (now on DockerHub) to **AWS ECS** (Elastic Container Service). By following these **step-by-step** instructions, you’ll have a public endpoint to access your API (and Swagger UI) online.

---

# **Activity 3 (Individual): Deploy Your API to AWS ECS**

## **Prerequisites**

1. **AWS Account**  
   - You must have an AWS account (free tier). Log in to the [AWS Console](https://aws.amazon.com/console/), click the right above white button `Sign In to the Console`.
2. **Docker Image on DockerHub**  
   - You should have already pushed your image to DockerHub, e.g. `docker push <your_dockerhub_id>/bookapp:1.0`.
3. **Security and Networking**  
   - You’ll need to create or use an existing **Key Pair** if you’re using an **EC2** cluster.  
   - For **Fargate** (serverless containers), no direct key pair is required. You’ll still need a **VPC** (usually the default VPC) and **security group** that allows inbound traffic on your chosen port (e.g., 80 or 8000).

> **Note**: This guide uses **Fargate** with a publicly accessible service. If you prefer **EC2** launch type or a load balancer, the steps are similar, but you’ll adapt some details.

---

## **Step 1: Create or Verify a Cluster**

1. **Go to ECS**  
   - In the AWS Console, search for “ECS” and open **Amazon Elastic Container Service**.
2. **Create a Cluster**  
   - Click **“Clusters”** on the left, then **“Create Cluster”**.
   - **Choose** “AWS Fargate (serverless)”
   - Give it a name, e.g., `bookapp-cluster`.
   - Leave default settings (VPC, subnets, etc.) if you’re okay with the default VPC and subnets.  
   - Click **Create**.  
   - You should see a success message that your cluster is created.

> If you already have a suitable Fargate cluster, you can skip creating a new one and reuse it.

---

## **Step 2: Create a Task Definition**

A **Task Definition** tells ECS how to run your container.

1. **Click “Task Definitions”** in the left menu.  
2. **Create new Task Definition**  
   - **Launch type**: Select **FARGATE**.  
   - **Task definition name**: e.g., `bookapp-taskdef`.
3. **Task Role**: Typically “None” unless your container needs AWS API permissions.  
4. **Operating system/Architecture**: Choose same `OS/ARCH` as your image, like `Linux/ARM64`, or `Linux/X86_64`, **Network Mode**: `awsvpc`.
5. **Task execution role**: Use the default or create a new one if prompted (it allows ECS to pull images from DockerHub).
6. **Container**:
   - Under **“Container definitions”** click **Add container**.  
   - **Container name**: e.g., `bookapp-container`.  
   - **Image**: `<your_dockerhub_id>/bookapp:1.0`  
     - Example: `myuser/bookapp:1.0`.  
   - **Port mappings**: 
     - Container port **8000** (assuming your FastAPI runs on port 8000).  
       - Protocol: `tcp`.
   - Scroll down and **save** container configuration.
7. **Task Size**:
   - Choose minimal requirements, e.g., **2GB** memory and **1 vCPU** for a small test.
8. **Review** and **Create** the task definition.

---

## **Step 3: Create a Service**

We create a **Service** so ECS runs and maintains our task. This ensures your app stays up even if the container restarts.

1. **Go back to Clusters** → select your cluster (`bookapp-cluster` if you made it).  
2. **Click “Services”** → “Create”  
   - **Launch type**: FARGATE  
   - **Task Definition**: Choose the one you just created (`bookapp-taskdef`), and the revision (likely `:1`).
   - **Platform version**: `LATEST`
   - **Service name**: e.g., `bookapp-service`
   - **Number of tasks**: 1 (for testing).
3. **Deployment type**: Rolling update is fine.  
4. **Networking**:  
   - **Cluster VPC**: default VPC (unless you have a custom one).  
   - **Subnets**: select at least one public subnet.  
   - **Security Group**: Select "Create a new security group" and configure it to **allow inbound traffic** on your container's port (e.g., 8000).  
   - Set up a new **Inbound Rule** for the security group to allow inbound traffic on port 8000. For testing purposes, you can choose:
      - **Type**: `ALL TCP`  
      - **Source**: `Anywhere`
   - **Auto-assign public IP**: **ENABLED** (so you get a public IP).  
5. **Load balancer**: For a quick test, you can choose **“None”**. If you want to run multiple tasks behind a load balancer, you’d choose Application Load Balancer, but that’s more steps.
6. **Click “Next step”** → skip any optional configurations → **Create Service**.

You’ll see ECS spin up a new container in your cluster. It shows "bookapp-service deployment is in progress. It takes a few minutes." Wait until the service’s status says **“Running”** or **“Active.”**

---

## **Step 4: Find Your Public IP and Test**

1. After the service stabilizes, go to **Clusters** → `bookapp-cluster` → click on the **Tasks** tab.  
2. You should see a running task. Click its **Task ID**.  
3. Scroll to **Configuration** details. Look for **Public IP** or **ENI** details. 
   - If you see “private IP” only, you might have disabled “Auto-assign public IP.”  
   - If you have a public IP, copy it.

4. **Open** your browser to `http://<PUBLIC_IP>:8000/docs`  
   - If your container listens on port 8000, that’s where you can see the **Swagger UI** by default in FastAPI.
   - You should see your **FastAPI** interactive docs.  
   - If you have a route `/books`, try `http://<PUBLIC_IP>:8000/books`.

> **Troubleshooting**  
> - If you get a timeout, check that your **security group** inbound rules **allow** port 8000 from `0.0.0.0/0`.  
> - Check the logs in ECS (click the **Logs** tab for the container) to see if uvicorn started successfully.

---

## **Step 5: Verify Everything Works**

- **Swagger UI** loads at `/docs`.  
- Any endpoints you created, like `/books`, should return the correct data if your container is functioning.

---

## **Recap**

1. **Push the Image** to DockerHub (done in Activity 2).  
2. **Create ECS Resources**:
   - **Cluster** (Fargate).  
   - **Task Definition** referencing your DockerHub image and container port.  
   - **Service** that runs the task with a public IP.  
3. **Test** using the **Public IP** on port **8000**, hitting `/docs` for Swagger.

Once deployed, your **FastAPI** app is publicly accessible at that IP. You can share the link with classmates or instructors for demonstration. If you want a domain or TLS, you can set up an **AWS Application Load Balancer** or use **Route 53** with your own domain. But for a simple lab demonstration, the public IP is enough to show your container is live in ECS.

# **Done!**

By completing this **Activity 3**:
- You have **ECS** up and running a container from your **DockerHub** repository.  
- You can open **Swagger UI** at `http://<PUBLIC_IP>:8000/docs` to test your routes.  
