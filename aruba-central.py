from pycentral.base import ArubaCentralBase


class ArubaCentral:
    """
    TODO: Docstring
    """
    def __init__(self, central_info, ssl_verify=True):
        self.central_info = central_info
        self.ssl_verify = ssl_verify
        self.central = ArubaCentralBase(central_info=self.central_info,
                                        ssl_verify=self.ssl_verify)

    def get_ap_status(self, macaddr):
        """
        Is the device reachable (up/down)?
        :param macaddr: String, MAC address of the AP
        :return: Status of the AP
        """
        apiPath = "/monitoring/v2/aps"
        apiMethod = "GET"
        apiParams = {
            "macaddr": macaddr,
            "fields": "status"
        }
        # TODO: determine how to reach the status of the AP
        response = self.central.command(apiMethod=apiMethod,
                                   apiPath=apiPath,
                                   apiParams=apiParams)["aps"][0]["status"]
        return response

    def get_template(self, serial_numbers):
        # Identifying which templates are assigned to devices

        apiPath = "/configuration/v1/devices/template"
        apiMethod = "GET"
        apiParams = {
            "device_serials": serial_numbers
        }
        response = self.central.command(apiMethod=apiMethod,
                                   apiPath=apiPath,
                                   apiParams=apiParams)["data"]
        response_sn_template = {}
        for sn in response:
            response_sn_template[sn] = response[sn]["template_name"]
        return response_sn_template

    def get_template_info(self):
        # Retrieve the content of the templates (rendered)
        apiPath = "/configuration/v1/groups/group/templates"
        apiMethod = "GET"
        apiParams = {
            "limit":"20",
            "offset":"0"
        }
        response = self.central.command(apiMethod=apiMethod,
                                   apiPath=apiPath,
                                   apiParams=apiParams)["data"]
        return response

    def get_template_sync_status(self, device_serial):
        # Is the device synchronised with the template

        apiPath = f"/configuration/v1/devices/{device_serial}/config_details"
        apiMethod = "GET"
        apiParams = {"details":"true"}
        response = self.central.command(apiMethod=apiMethod,
                                   apiPath=apiPath,
                                   apiParams=apiParams)
        return response

    def get_connected_lldp_device(self):
        # Identifying which devices is connected to the trunk via LLDP
        pass

    def get_ssid_broadcasted(self):
        # Which SSID are being broadcasted
        apiPath = "/rapids/v1/ssid_allow"
        apiMethod = "GET"

        response = self.central.command(apiMethod=apiMethod,
                                   apiPath=apiPath)
        return response


central_info = {
    "base_url": "<api-gateway-domain-url>",
    "token": {
        "access_token": "<api-gateway-access-token>"
    }
}

a = ArubaCentral(central_info)
# print(a)
# print(a.central_info)
# print(a.ssl_verify)
# print(a.central)

# Tests
mac = "MAC address"
sn = "Serial Number"
print(a.get_ap_status(mac))
print(a.get_template(sn))
print(a.get_template_info())
print(a.get_template_sync_status(sn))
# print(a.get_connected_lldp_device())
print(a.get_ssid_broadcasted())