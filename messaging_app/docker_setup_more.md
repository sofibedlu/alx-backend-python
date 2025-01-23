# Docker and Docker Compose

## docker setup
### Create a requirements.txt File
- The requirements.txt file lists all the Python dependencies your Django project needs.
    ```bash
       pip freeze > requirements.txt

### Install Docker for Linux
- use official docker installation from https://docs.docker.com/engine/install/

### Create a Dockerfile in the Project Root
- The Dockerfile contains instructions to build your Docker image.

### Build the Docker Image
- Navigate to the root directory of your project and run the following command to build your Docker image
    ```bash
       docker build -t messaging-app .
- from the root directory where the Dockerfile resides.


## docker compose
- Manages multi-container Docker applications, defining services, networks, and volumes.

### **key Components:**
- **Services:** in our current docker-compose.yml
    - web: Django application service.
        - build: Builds using the provided Dockerfile.
        - command: Runs the Django development server.
        - volumes: Mounts the current directory to /app in the container for real-time code synchronization.
        - ports: Maps host port 8020 to container port 8000.
        - env_file: Loads environment variables from .env.
        - depends_on: Ensures db service starts before web.
    - db: MySQL database service.
        - image: Uses MySQL 8.0 official image.
        - restart: Always restarts the container on failure.
        - environment: Configures MySQL using environment variables.
        - ports: Maps host port 3307 to container port 3306.
        - volumes: Persists MySQL data using db_data volume.
        - command: Sets MySQL authentication plugin for compatibility.
    - Volumes:
        - db_data: Named volume to persist MySQL data across container restarts.

- **Container Naming Confusion**
    - Docker Compose names containers using the format: <project_name>-<service_name>-<instance_number>.

- 

### Essential Docker Commands

Here are some fundamental Docker commands to manage your containers, images, volumes, and more. Familiarizing yourself with these commands will help you effectively work with Docker in your development workflow.

#### **1. Docker Compose Commands**

- **Build Docker Images**

    Builds the Docker images defined in your `docker-compose.yml` file.

    ```sh
    docker compose build
    ```

- **Run Containers in Detached Mode**

    Starts the containers in the background.

    ```sh
    docker compose up -d
    ```

- **View Running Containers**

    Lists all containers that are currently running.

    ```sh
    docker compose ps
    ```

- **Stop and Remove Containers**

    Stops and removes the containers, networks, and default volumes defined in your [docker-compose.yml](http://_vscodecontentref_/0).

    ```sh
    docker compose down
    ```

- **Stop Containers Without Removing Them**

    Stops the running containers without removing them.

    ```sh
    docker compose stop
    ```

- **Start Stopped Containers**

    Starts containers that have been stopped.

    ```sh
    docker compose start
    ```

- **View Container Logs**

    Displays logs for a specific service.

    ```sh
    docker compose logs web
    docker compose logs db
    ```

- **Execute Commands Inside a Container**

    Runs a command inside a running container.

    ```sh
    docker compose exec web bash
    docker compose exec db bash
    docker compose exec web python manage.py migrate
    docker compose exec web python manage.py createsuperuser
    ```

- **Scale Services**

    Adjusts the number of running containers for a specific service.

    ```sh
    docker compose up --scale web=3 -d
    ```

- **Remove Containers and Volumes**

    Stops and removes containers along with their associated volumes.

    ```sh
    docker compose down -v
    ```

#### **2. Basic Docker Commands**

- **List All Docker Containers**

    Shows all containers (running and stopped).

    ```sh
    docker ps -a
    ```

- **List Running Docker Containers**

    Displays only the containers that are currently running.

    ```sh
    docker ps
    ```

- **Start a Docker Container**

    Starts a stopped container.

    ```sh
    docker start <container_name_or_id>
    ```

- **Stop a Docker Container**

    Stops a running container.

    ```sh
    docker stop <container_name_or_id>
    ```

- **Remove a Docker Container**

    Deletes a container. The container must be stopped first.

    ```sh
    docker rm <container_name_or_id>
    ```

- **List All Docker Images**

    Displays all Docker images on your system.

    ```sh
    docker images
    ```

- **Remove a Docker Image**

    Deletes an image from your system.

    ```sh
    docker rmi <image_name_or_id>
    ```

- **Pull a Docker Image**

    Downloads an image from Docker Hub.

    ```sh
    docker pull <image_name>
    ```

- **Push a Docker Image**

    Uploads an image to Docker Hub.

    ```sh
    docker push <image_name>
    ```

- **View Docker Container Logs**

    Retrieves logs from a specific container.

    ```sh
    docker logs <container_name_or_id>
    ```

- **Execute a Command in a Running Container**

    Runs a command inside an active container.

    ```sh
    docker exec -it <container_name_or_id> <command>
    ```

    *Example:*

    ```sh
    docker exec -it messaging_app-web-1 bash
    ```

- **Inspect Docker Volumes**

    Provides detailed information about a specific volume.

    ```sh
    docker volume inspect db_data
    ```

- **List All Docker Volumes**

    Shows all Docker-managed volumes on your system.

    ```sh
    docker volume ls
    ```

- **Remove Unused Docker Volumes**

    Deletes all volumes not currently used by any containers.

    ```sh
    docker volume prune
    ```

- **View Detailed Docker System Information**

    Displays system-wide information including Docker version, storage drivers, etc.

    ```sh
    docker info
    ```

- **Clean Up Unused Docker Objects**

    Removes unused data such as stopped containers, dangling images, and unused networks.

    ```sh
    docker system prune
    ```

    *Use with caution as this will delete data:*

    ```sh
    docker system prune -a
    ```

#### **3. Docker Networking Commands**

- **List Docker Networks**

    Displays all Docker networks on your system.

    ```sh
    docker network ls
    ```

- **Inspect a Docker Network**

    Provides detailed information about a specific network.

    ```sh
    docker network inspect <network_name>
    ```

- **Connect a Container to a Network**

    Attaches a container to an existing network.

    ```sh
    docker network connect <network_name> <container_name_or_id>
    ```

- **Disconnect a Container from a Network**

    Detaches a container from a network.

    ```sh
    docker network disconnect <network_name> <container_name_or_id>
    ```

#### **4. Docker Volume Backup and Restore**

- **Backup a Docker Volume**

    Creates a backup of a specific volume.

    ```sh
    docker run --rm -v db_data:/data -v $(pwd):/backup alpine tar cvf /backup/db_data_backup.tar /data
    ```

- **Restore a Docker Volume**

    Restores data to a specific volume from a backup.

    ```sh
    docker run --rm -v db_data:/data -v $(pwd):/backup alpine tar xvf /backup/db_data_backup.tar -C /data
    ```

#### **5. Docker Compose Health Checks**

- **View Service Health Status**

    If health checks are configured, you can view the health status of services.

    ```sh
    docker compose ps
    ```

    **Sample Output:**

    ```
          Name                     Command               State                Ports
    ----------------------------------------------------------------------------------------
    messaging_app_db_1   docker-entrypoint.sh --def ...   Up (healthy)      0.0.0.0:3307->3306/tcp
    messaging_app_web_1  python manage.py runserver ...   Up (healthy)      0.0.0.0:8020->8000/tcp
    ```

#### **6. Docker Compose Override Files**

- **Use Override Files for Development**

    Docker Compose allows you to have multiple Compose files for different environments.

    - **Default Behavior:**

        ```sh
        docker compose -f docker-compose.yml -f docker-compose.override.yml up -d
        ```

    - **Custom Override:**

        ```sh
        docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
        ```

#### **7. Viewing and Managing Docker Resources**

- **List All Containers (Including Stopped Ones)**

    ```sh
    docker ps -a
    ```

- **List All Images**

    ```sh
    docker images -a
    ```

- **List All Volumes**

    ```sh
    docker volume ls
    ```

- **List All Networks**

    ```sh
    docker network ls
    ```

#### **8. Docker System Commands**

- **Check Docker Version**

    ```sh
    docker --version
    docker compose --version
    ```

- **View Docker Disk Usage**

    ```sh
    docker system df
    ```

- **Display Detailed Docker Information**

    ```sh
    docker info
    ```

#### **9. Docker Compose Scaling**

- **Scale Services Up or Down**

    Adjust the number of container instances for a service.

    ```sh
    docker compose up --scale web=3 -d
    ```

    - **Example:** Scales the `web` service to 3 instances.

- **Remove All Scaled Instances**

    Reduce the service to its default scale (defined in [docker-compose.yml](http://_vscodecontentref_/1)).

    ```sh
    docker compose up --scale web=1 -d
    ```

#### **10. Cleaning Up Docker Resources**

- **Remove All Stopped Containers, Unused Networks, Images, and Build Cache**

    ```sh
    docker system prune -a
    ```

    *Use with caution as this will delete all unused data.*

---