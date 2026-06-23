import niquests
from src.utils.constants import DNAC_URL, DNAC_USERNAME, DNAC_PASSWORD


class AsyncDnacClient:
    """An asynchronous client library for interacting with Cisco DNA Center.

    This client leverages the `niquests` library to execute asynchronous HTTP requests
    against the Cisco DNA Center Intent and System APIs. It uses an async factory pattern
    for secure initialization and supports the async context manager protocol to ensure Proper 
    session connection teardown, making it optimal for execution environments like Temporal.

    Attributes:
        base_url (str): The destination base URL for the DNA Center cluster environment.
        token (str): The valid internal JWT authentication token used for API authorizations.
        session (niquests.AsyncSession): The active underlying HTTP pool configuration.
    """

    def __init__(self, token: str):
        """Initializes the AsyncDnacClient with an explicit authentication token.

        Args:
            token: A valid JWT token retrieved from the DNA Center authentication endpoint.
        """
        self.base_url = DNAC_URL
        self.token = token
        self.session = niquests.AsyncSession()
        self.session.headers.update(
            {
                "X-Auth-Token": self.token,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    @classmethod
    async def create(cls):
        """Asynchronous factory to authenticate and return an initialized client instance.

        This method should be utilized instead of direct class instantiation to prevent 
        synchronous blocking calls during authentication network I/O, which is crucial 
        when spawning instances within Temporal activity workers.

        Returns:
            AsyncDnacClient: An authenticated instance of the client with a populated session.

        Raises:
            niquests.exceptions.HTTPError: If the authentication request fails or returns a
                non-2xx status code.
        """
        base_url = DNAC_URL
        url = f"{base_url}/dna/system/api/v1/auth/token"

        # Use an ephemeral async session to retrieve the initial token
        async with niquests.AsyncSession() as auth_session:
            response = await auth_session.post(
                url=url, auth=(DNAC_USERNAME, DNAC_PASSWORD), verify=False
            )
            response.raise_for_status()
            token = response.json()["Token"]

        return cls(token=token)

    async def __aenter__(self):
        """Enters the asynchronous runtime context manager.

        Returns:
            AsyncDnacClient: The current client instance bound to the context lifecycle.
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exits the asynchronous runtime context manager and disposes resources.

        Closes the underlying HTTP connection pools within the active niquests session.
        """
        await self.session.close()

    async def get_network_devices(self) -> list:
        """Retrieves inventory details for all network devices managed by DNA Center.

        Returns:
            list: A list of dictionaries, where each dictionary represents a managed 
                network device asset and its associated inventory metadata.

        Raises:
            niquests.exceptions.HTTPError: If the DNA Center API returns an invalid 
                or non-2xx operational status code.
        """
        url = f"{self.base_url}/dna/intent/api/v1/network-device"
        response = await self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json().get("response", [])

    async def get_device_interfaces(self, device_id: str) -> list:
        """Retrieves all interface configuration profiles for a targeted device ID.

        Commonly used as an architectural block for compiling structural telemetry 
        auditing checks or zero-touch provisioning status verifications.

        Args:
            device_id: The unique UUID string of the target network device.

        Returns:
            list: A list of dictionaries containing individual interface attributes, 
                speeds, operational states, and naming conventions.

        Raises:
            niquests.exceptions.HTTPError: If the execution fails or the provided
                device ID cannot be processed by the API gateway.
        """
        url = f"{self.base_url}/dna/intent/api/v1/interface"
        params = {"deviceId": device_id}
        response = await self.session.get(url, params=params, verify=False)
        response.raise_for_status()
        return response.json().get("response", [])

    async def get_device_health(self) -> list:
        """Retrieves systemic health scores and uptime metrics for the managed topology.

        This API aggregates device subsystem states, and is ideal for running structured 
        pre-check and post-check evaluations inside Temporal automation maintenance workflows.

        Returns:
            list: A collection of health score parameters and packet delivery metrics 
                categorized by individual infrastructure assets.

        Raises:
            niquests.exceptions.HTTPError: If connection errors or API tracking anomalies occur.
        """
        url = f"{self.base_url}/dna/intent/api/v1/device-health"
        response = await self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json().get("response", [])

    async def run_read_only_command(self, device_id: str, command: str) -> str:
        """Executes a non-interactive operational CLI command on a targeted device asset.

        Because DNA Center processes CLI requests asynchronously via an internal execution queue,
        this method returns a tracked Task UUID immediately. This aligns perfectly with 
        Temporal's polling and activity heartbeating patterns.

        Args:
            device_id: The unique UUID string of the target network device.
            command: The exact string value of the read-only command (e.g., 'show version').

        Returns:
            str: A unique task identifier string used to poll for the completed output execution.

        Raises:
            niquests.exceptions.HTTPError: If authorization fails or the command request is rejected.
        """
        url = (
            f"{self.base_url}/dna/intent/api/v1/network-device-poller/cli/read-request"
        )
        payload = {"commands": [command], "deviceUuids": [device_id]}
        response = await self.session.post(url, json=payload, verify=False)
        response.raise_for_status()
        return response.json().get("response", {}).get("taskId")

    async def get_task_status(self, task_id: str) -> dict:
        """Checks the internal tracking state of an asynchronous DNA Center operation.

        This method provides an operational checkpoint loop designed to be continuously 
        polled inside an elongated or long-running Temporal Activity execution container.

        Args:
            task_id: The unique string identifier assigned to an uncompleted asynchronous task.

        Returns:
            dict: An execution dictionary payload specifying parameters like 'progress', 
                'endTime', 'isError', or execution output details if completed.

        Raises:
            niquests.exceptions.HTTPError: If the tracking endpoint is unreachable or 
                the specified task ID is structurally invalid.
        """
        url = f"{self.base_url}/dna/intent/api/v1/task/{task_id}"
        response = await self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json().get("response", {})


# --- Execution Sandbox for testing locally ---
if __name__ == "__main__":
    import asyncio
    from pprint import pprint

    async def main():
        print("Authenticating with DNA Center asynchronously...")
        # Utilize the async context manager strategy to keep connections clean
        async with await AsyncDnacClient.create() as client:
            print("\n--- Fetching Network Devices ---")
            devices = await client.get_network_devices()
            pprint(devices[:2])  # Print out the first couple items to verify

            if devices:
                target_device = devices[0].get("id")
                print(
                    f"\n--- Checking Health Status for Target Device ID: {target_device} ---"
                )
                health = await client.get_device_health()
                pprint(health[:1])

    asyncio.run(main())