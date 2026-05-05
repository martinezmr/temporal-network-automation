import niquests
from src.utils.constants import DNAC_URL, DNAC_USERNAME, DNAC_PASSWORD


class DnacClient:
    def __init__(self):
        self.base_url = DNAC_URL
        self.username = DNAC_USERNAME
        self.password = DNAC_PASSWORD
        self.session = niquests.Session()
        self.token = self._get_token()
        # Update session headers with the token
        self.session.headers.update({"X-Auth-Token": self.token})

    def _get_token(self):
        """Authenticates and retrieves the mandatory JWT token."""
        url = f"{self.base_url}/dna/system/api/v1/auth/token"
        # DNAC expects Basic Auth ONLY on the token endpoint
        response = self.session.post(
            url=url, auth=(self.username, self.password), verify=False
        )
        response.raise_for_status()
        return response.json()["Token"]

    def get_network_devices(self):
        """Now uses the token stored in the session headers."""
        url = f"{self.base_url}/dna/intent/api/v1/network-device"
        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()["response"]


# if __name__ == "__main__":
#     client = DnacClient()
#     devices = client.get_network_devices()
#     from pprint import pprint
#     pprint(devices)
