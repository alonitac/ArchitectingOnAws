# Docker tutorials

## Get Docker

#### Windows users

[Docker Desktop](https://docs.docker.com/desktop/install/windows-install/) is an easy-to-install application for your Mac or Windows environment that enables you to build and share containerized applications and microservices.

Docker Desktop includes:

- Docker Engine
- Docker CLI client
- Docker Compose
- More...

**If you installed Docker locally on Windows 10**, make sure the Hyper-V and Containers features are installed and enabled:
1. Right-click the **Windows Start** button and choose **Apps and Features**.
2. Click the **Programs and Features** link (a small link on the right).
3. Click **Turn Windows features on or off**.
4. Check the **Hyper-V** and **Containers** checkboxes and click **OK**.

![](../.img/dockerwin10.png)


#### Linux users

Install [Docker Engine](https://docs.docker.com/engine/install/ubuntu/) and [Docker Compose](https://docs.docker.com/compose/install/compose-plugin/)

You may want to add your Linux user to `docker` group:
```shell
sudo usermod -aG docker $USER
```

---

Verify Docker installed by:
```shell
docker version
```

Expect output similar to:
```text
Client: Docker Engine - Community
 Version:           20.10.14
 API version:       1.41
 Go version:        go1.16.15
 Git commit:        a224086
 Built:             Thu Mar 24 01:47:57 2022
 OS/Arch:           linux/amd64
 Context:           default
 Experimental:      true

Server: Docker Engine - Community
 Engine:
  Version:          20.10.14
  API version:      1.41 (minimum version 1.12)
  Go version:       go1.16.15
  Git commit:       87a90dc
  Built:            Thu Mar 24 01:45:46 2022
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.5.11
  GitCommit:        3df54a852345ae127d1fa3092b95168e4a88e2f8
 runc:
  Version:          1.0.3
  GitCommit:        v1.0.3-0-gf46b6ba
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
```

## Pull and run images

In this tutorial you will run Nginx server in a Docker container and familiarize yourself with the basic commands set of Docker.  

1. Pull the [nginx:latest](https://hub.docker.com/_/nginx/) image by:
```shell
docker pull nginx:latest
```

Most of your images will be created on top of a base image from the [Docker Hub](https://hub.docker.com/) registry.
Docker Hub contains many pre-built images that you can `pull` and try without needing to define and configure your own.
To download a particular image, or set of images (i.e., a repository), use `docker pull <image-name>:<image-tag>`.

2. Run it by
```shell
docker run -p 8080:80 --name nginx-1 nginx:latest
```

The `docker run` launches a new container. 

3. Execute `docker ps`. How many containers are currently running on your system?

`docker ps` lists containers. Use with `-a` to list all containers (including stopped). It is very useful command to get the status of you running and stopped containers. 

4. Stop the running Nginx container by `docker stop <container-name or container-id>`.
5. Start is again by `docker start <name or id>`
6. Kill the running container by `docker kill <name or id>`.

The `docker kill` command kills one or more running containers. Note that kill command doesn't remove the container from your system but only stop it.
In order to clean up the terminated containers use the `docker rm <name or id>` command.

### Communication between containers and the internet

7. Start two different Nginx servers, as follows:
   1. Container called `nginx-1` listening of port `8080`.
   2. Container called `nginx-2` listening of port `8081`.
8. Make sure both servers are accessible from your browser.
9. Get the internal IP of `nginx-1` by `docker inspect nginx-1`.
10. Get a Shell access to `nginx-2` by `docker exec -it nginx-2 /bin/bash`.

The [`docker exec`](https://docs.docker.com/engine/reference/commandline/exec/) command allows you to run a command in a **running container**.

10. **Within `nginx-2` Shell**, install the `ping` cli tool by:
```shell
apt update && apt install iputils-ping
```

11. Try to ping the IP of `nginx-1`.
12. Try to ping `google.com`.

## Containerizing an app

In this tutorial, we will be working with a simple "YouTube chat" that is running in Python. If you’re not familiar with Python, don’t worry. No real experience is needed.
The application source code in under `app-monolith`. 

In order to build the application, we need to use a `Dockerfile`. A Dockerfile is simply a text-based script of instructions that is used to create a container image.

1. In `app-monolith` directory, create a file named `Dockerfile` with the following contents:
```dockerfile
FROM python:3.8.12-slim-buster
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python3", "app.py"]
```
Please check that the file `Dockerfile` has no file extension like `.txt`.

2. Open a terminal and go to the app directory with the `Dockerfile`. Now build the container image using the `docker build` command:
```shell
docker build -t app-monolith:0.0.1 .
```

This command used the Dockerfile to build a new container image. 
You might have noticed that a lot of “layers” were downloaded. This is because we instructed the builder that we wanted to start from the `python:3.8.12-slim-buster` image.
But, since we didn’t have that on our machine, that image needed to be downloaded.

After the image was downloaded, we copied in our application and used `pip` to install our application’s dependencies. The `CMD` directive specifies the default command to run when starting a container from this image.
Finally, the `-t` flag tags our image. Think of this simply as a human-readable name for the final image. Since we named the image `app-monolith:0.0.1`, we can refer to that image when we run a container.

The `.` at the end of the docker build command tells Docker that it should look for the Dockerfile in the current directory.

Now that we have an image, let’s run the application. To do so, we will use the `docker run` command (remember that from earlier?).

3. Start your container by:
```shell
docker run -d -p 8080:8080 app-monolith:0.0.1
```
Note the `-d` which runs the container in background, releasing the CMD terminal.


4. After a few seconds, open your web browser to `http://localhost:8080`.

#### Update the application

Let’s make the change to our application.

5. In the `app-monolith/templates/index.html` file, update line 13 to be.
```text
- Welcome to the YouTube chat!
+ Welcome to the YouTube chat - IEC 2022 Architecture Course!
```

6. Let’s build our updated version of the image, using the same command we used before.
```shell
docker build -t app-monolith:0.0.2 .
```

7. Let’s start a new container using the updated code.
```shell
docker run -d -p 8080:8080 app-monolith:0.0.2
```

**Uh oh!** You probably saw an error from the docker daemon.
We aren’t able to start the new container because our old container is still running. It is because the container is using the host’s port 8080 and only one process on the machine (containers included) can listen to a specific port. To fix this, we need to remove the old container.

8. Remove the container:
```shell
docker ps 

# get the container id... 

docker stop <the-container-id>
docker rm <the-container-id>
```

#### Persist data using volume mounting

By default, the app stores its data in a SQLite Database at `/app/data/videos.db` in the container’s filesystem.
If you’re not familiar with SQLite, no worries! It’s simply a relational database in which all of the data is stored in a single file.

In case you didn’t notice, your chat videos are being wiped clean every single time we launch the container. Why is this?

If a directory in the container is **mounted**, changes in that directory are also seen on the host machine. If we mount that same directory across container restarts, we’d see the same files.

1. Make sure you don’t have any previous `app-monolith` containers running.
2. Run the following command from the app directory. We’ll explain what’s going on afterwards.
```shell
docker run -p 8080:8080 -v "$(pwd)/data:/app/data" app-monolith:0.0.2 
```
Note the `-v "$(pwd)/data:/app/data"` which mounts the data directory from the host into the `/app/data` directory in the container.
3. Test your app and verify that the data persists.

## Multiple-container app

In general, each container should do one thing and do it well. A few reasons:

 - There’s a good chance you’d have to scale APIs and front-ends differently than databases
 - Separate containers let you version and update versions in isolation
 - While you may use a container for the database locally, you may want to use a managed service for the database in production. You don’t want to ship your database engine with your app then.

So, we will update our application to work like this:

![](../.img/compose-app.png)

So, how do we allow one container to talk to another? The answer is networking. Now, you don’t have to be a network engineer (hooray!). Simply remember this rule...

**If two containers are on the same network, they can talk to each other. If they aren’t, they can’t.**

1. Create a virtual Docker network:
```shell
docker network create app-multi
```
2. Start a MySQL container and attach it to the network. We’re also going to define a few environment variables that the database will use to initialize the database:
```shell
docker run --network app-multi --network-alias mysql -v $(pwd)/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=secret -e MYSQL_DATABASE=videos mysql:5.7
```
3. Verify MySql is accessible from another container. To figure it out, we’re going to make use of the [nicolaka/netshoot](https://github.com/nicolaka/netshoot) container, which ships with a lot of tools that are useful for troubleshooting or debugging networking issues.
```shell
docker run -it --network app-multi nicolaka/netshoot
```
4. Inside the container, we’re going to use the dig command, which is a useful DNS tool. We’re going to look up the IP address for the hostname mysql.
```shell
dig mysql
```
And make sure that `mysql` is being resolved to the IP address of the container.
5. Using the above `docker build` command, build a new image from the app `app-multi` directory (Dockerfile already there), run it by:
```shell
docker run --network app-multi -p 8082:8080 app-multi:0.0.1
```
6. Test the app.

## Docker compose

[Docker Compose](https://docs.docker.com/compose/) is a tool that was developed to help define and share multi-container applications. With Compose, we can create a YAML file to define the services and with a single command, can spin everything up or tear it all down.
Let's deploy out app using Docker compose.

1. Make sure Docker compose is installed:
```shell
docker-compose version
```
2. At the root of the app project, create a file named `docker-compose.yml`.
3. In the compose file, we’ll start off by defining the schema version. In most cases, it’s best to use the latest supported version.
```yaml
version: "3.7"
```
4. Next, we’ll define the list of services (or containers) we want to run as part of our application.
```yaml
version: "3.7"

services:
```

#### Define the `app-multi` service

5. Looking at the `docker run` command for the `app-multi`, let’s define the service entry and the image for the container. We can pick any name for the service.
```yaml
version: "3.7"

services:
  app:
    image: app-multi:0.0.1
```
6. Let’s migrate the `-p 8082:8080` part of the command by defining the ports for the service.
```yaml
version: "3.7"

services:
  app:
    image: app-multi:0.0.1
    ports:
       - 8082:8080
```

#### Define `mysql` service

7. We will first define the new service and name it mysql so it automatically gets the network alias. We’ll go ahead and specify the image to use as well.
```yaml
version: "3.7"

services:
  app:
    # The app service definition
  mysql:
    image: mysql:5.7
```
8. Next, we’ll define the volume mapping. We need to define the volume in the top-level `volumes:` section and then specify the mountpoint in the service config.
```yaml
version: "3.7"

services:
  app:
    # The app service definition
  mysql:
    image: mysql:5.7
    volumes:
       - mysql-data:/var/lib/mysql
volumes:
   mysql-data:
```
while changing `<your-local-path>` to the path you want to mount in the host machine.

9. Finally, we only need to specify the environment variables.
```yaml
version: "3.7"

services:
   app:
     image: app-multi:0.0.1
     ports:
        - 8082:8080
   mysql:
    image: mysql:5.7
    volumes:
       - mysql-data:/var/lib/mysql
    environment:
       MYSQL_ROOT_PASSWORD: secret
       MYSQL_DATABASE: videos
volumes:
   mysql-data:
```

At this point, our complete `docker-compose.yml` should look like this:
```yaml
version: "3.7"

services:
  app:
    # The app service definition
  mysql:
    image: mysql:5.7
    volumes:
       - mysql-data:/var/lib/mysql
    environment:
       MYSQL_ROOT_PASSWORD: secret
       MYSQL_DATABASE: videos
volumes:
   mysql-data:
```

#### Run the application stack

Now that we have our docker-compose.yml file, we can start it up!

10. Make sure no other copies of the app/db are running first (`docker ps` and `docker rm -f <ids>`).
11. Start up the application stack using the `docker-compose up` command.
12. When you’re ready to tear it all down, simply run `docker-compose down`.


## Security scanning

When you have built an image, it is a good practice to scan it for security vulnerabilities using the `docker scan` command. Docker has partnered with [Snyk](https://snyk.io/) to provide the vulnerability scanning service.

You must be logged in to Docker Hub to scan your images.
Run the command `docker scan --login`, and then scan your images using `docker scan <image-name>`.

## Inspect Docker networking options

#### Use `host` networking (only works on Linux hosts)

If you use the `host` network mode for a container, that container’s network stack is not isolated from the Docker host (the container shares the host’s networking namespace),
and the container does not get its own IP-address allocated.
Generally, host mode networking can be useful to optimize performance, as it does not require network address translation (NAT), and no “userland-proxy” is created for each port. But keep in mind that using host mode has significant security implication!

1. Run the Nginx webserver in the host network
```shell
docker run --network host --name nginx-1 nginx:latest
```
2. Visit the webserver in `http://localhost`.


## Push docker image to AWS Elastic Container Registry (ECR)

Amazon Elastic Container Registry (Amazon ECR) is an AWS managed Docker container image registry service that is secure, scalable, and reliable.

A **repository** is where you store your Docker images in Amazon ECR\. Each time you push or pull an image from Amazon ECR, you specify the repository and the registry location which informs where to push the image to or where to pull it from\.

1. Open the Amazon ECR console at [https://console\.aws\.amazon\.com/ecr/](https://console.aws.amazon.com/ecr/).

2. Choose **Get Started**\, or **Repositories** and **Create repository**.

3. For **Visibility** settings, choose **Private**.

4. For **Repository name**, specify a name for the repository: `<your-name>-supportBot`, while changing `<your-name>` to your name.

6. Choose **Create repository**\.

**Build, tag, and push a Docker image**

1. Select the repository you created and choose **View push commands** to view the steps to push an image to your new repository\.

1. Run the login command that authenticates your Docker client to your registry by using the command from the console in a terminal window\. This command provides an authorization token that is valid for 12 hours\.

1. Build the image and tag it for your new repository\. Using the docker build command from the console in a terminal window\. Make sure that you are in the same directory as your Dockerfile\.

1. Tag the image with your Amazon ECR registry URI and your new repository by pasting the docker tag command from the console into a terminal window\. The console command assumes that your image was built from a Dockerfile in the previous step\. If you did not build your image from a Dockerfile, replace the first instance of `repository:latest` with the image ID or image name of your local image to push\.

1. Push the newly tagged image to your repository by using the docker push command in a terminal window\.

1. Choose **Close**\.
