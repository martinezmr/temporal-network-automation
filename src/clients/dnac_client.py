import niquests
from utils.constants import DNAC_BASE_URL, DNAC_USERNAME, DNAC_PASSWORD

class DnacClient:
    def __init__(self):
        self.base_url = DNAC_BASE_URL
        self.username = DNAC_USERNAME
        self.password = DNAC_PASSWORD       
        self.session = niquests.Niquests(self.base_url, auth=(self.username, self.password))

    def get_network_devices(self):
        url = f"{self.base_url}/dna/intent/api/v1/network-device"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    async def get_network_devices_async(self):
        url = f"{self.base_url}/dna/intent/api/v1/network-device"
        async with niquests.AsyncSession(self.base_url, auth=(self.username, self.password)) as session:
            response = await session.get(url)
            response.raise_for_status()
            return await response.json()