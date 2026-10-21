from utils.logger import setup_logger
import docker


class DockerManager:

    def __init__(self):
        self.logger = setup_logger("docker")
        self.logger.info("Docker Manager Initialized")

        self.client = docker.from_env()


    def start_container(self, container_name):
        try:
            container = self.client.containers.get(container_name)
            container.reload()
            if container.status != "running":
                self.logger.info(f"Starting Docker Container: {container_name}")
                container.start()
            else:
                self.logger.info(f"{container_name} is already running.")

        except docker.errors.NotFound:
            self.logger.error(f"{container_name} not found")


    def get_container_status(self, container_name):
        
        try:
            container = self.client.containers.get(container_name)
            container.reload()

            return container.status

        except docker.errors.NotFound:
            self.logger.error(f"{container_name} not found")


    def restart_container(self, container_name):
        try:
            self.logger.info(f"Restarting Docker Container: {container_name}")
            container = self.client.containers.get(container_name)
            container.restart()
            self.logger.info(f"{container_name} restarted successfully.")

        except docker.errors.NotFound:
            self.logger.error(f"{container_name} not found")


    def stop_container(self, container_name):
        try:
            container = self.client.containers.get(container_name)
            self.logger.info(f"Stopping {container_name}")
            container.stop()
            self.logger.info(f"{container_name} stopped successfully.")

        except docker.errors.NotFound:
            self.logger.error(f"{container_name} not found")
