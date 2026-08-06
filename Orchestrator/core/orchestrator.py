from utils.config_loader import load_config
from core.docker_manager import DockerManager
from utils.logger import setup_logger
import time


class Orchestrator:

    def __init__(self):

        self.logger = setup_logger("orchestrator")
        self.logger.info("Initializing Orchestrator...")

        self.config = load_config()
        self.honeypots = self.config["honeypots"]
        self.docker_manager = DockerManager()

    def start(self):

        self.logger.info("Starting Orchestrator...")

        self.start_honeypots()
        self.monitor()


    def start_honeypots(self):

        for name, details in self.honeypots.items():

            if details["enabled"]:
                self.docker_manager.start_container(details["container_name"])

            else:
                self.logger.info(f"Skipping {name} (Disabled)")


    def health_check(self):

       for name, details in self.honeypots.items():

            if not details["enabled"]:
                continue

            status = self.docker_manager.get_container_status(
                details["container_name"]
            )

            if status is None:
                continue

            elif status == "running":
                self.logger.info(f"{name} is running.")

            else:
                self.restart_honeypot(details["container_name"])


    def restart_honeypot(self, name):

        self.logger.warning(f"{name}  stopped. Restarting...")

        self.docker_manager.restart_container(name)


    def monitor(self):

        while True:
            self.health_check()
            time.sleep(30)


    def stop_honeypot(self, name):

        self.logger.info(f"Stopping {name}")

        self.docker_manager.stop_container(name)
