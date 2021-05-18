from pycentral.base import ArubaCentralBase
import requests
import json


class ArubaCentral:
    """
    This class allows to get various information from Aruba Central
    """
    def __init__(self, central_info, ssl_verify=True):
        self.central_info = central_info
        self.ssl_verify = ssl_verify
        self.central = ArubaCentralBase(central_info=self.central_info,
                                        ssl_verify=self.ssl_verify)

    # Unable to test without APs online
    def get_ap_status(self, serial_number):
        """
        Is the device reachable (up/down)?
        https://developer.arubanetworks.com/aruba-central/reference/ap-3#apiexternal_controllerget_aps_v2-2
        :param macaddr: String, MAC address of the AP
        :return: Status of the AP
        """
        apiPath = "/monitoring/v2/aps"
        apiMethod = "GET"
        apiParams = {
            "macaddr": serial_number,
            "fields": "status"
        }
        # TODO: determine how to reach the status of the AP
        response = self.central.command(apiMethod=apiMethod,
                                   apiPath=apiPath,
                                   apiParams=apiParams)["aps"][serial_number]["status"]
        return response

    #Tested
    def get_template(self, serial_number):
        """
        Identifying which templates are assigned to devices
        https://developer.arubanetworks.com/aruba-central/reference/devices-4#apidevicesget_devices_template_details-1
        :param serial_number: Serial number of the device
        :return: Template name assigned to the device
        """
        apiPath = "/configuration/v1/devices/template"
        apiMethod = "GET"
        apiParams = {
            "device_serials": serial_number
        }

        response = self.central.command(apiMethod=apiMethod,
                                   apiPath=apiPath,
                                   apiParams=apiParams)['msg']['data'][serial_number]['template_name']

        return response

    # Failed test. Output: {'code': 500, 'msg': {'description': 'Internal Server Error', 'error_code': '0001', 'service_name': 'Configuration'}}
    def get_template_info(self, serial_number):
        """
        Retrieve the content of the templates (rendered)
        https://developer.arubanetworks.com/aruba-central/reference/devices-4#apidevicesget_device_variabilised_template-1
        :param serial_number: Serial number of the device
        :return: Variablised template of the device
        """
        api_path = f"/configuration/v1/devices/{serial_number}/variablised_template"
        api_method = "GET"

        response = self.central.command(apiMethod=api_method,
                                   apiPath=api_path)
        return response

    # Tested
    def get_template_sync_status(self, serial_number):
        """
        Is the device synchronised with the template
        https://developer.arubanetworks.com/aruba-central/reference/devices-4#apidevicesget_device_configuration_details-1
        :param serial_number: Serial number of the device
        :return: Template error status (True or False)
        """
        api_path = f"/configuration/v1/devices/{serial_number}/config_details"
        api_method = "GET"
        api_params = {"details":"false"}
        headers = {"Accept": "application/json"}
        response = self.central.command(apiMethod=api_method,
                                   apiPath=api_path,
                                   apiParams=api_params, headers=headers)['msg']

        start = response.find('{')
        stop = response.find('}') + 1
        template_error_status = json.loads(response[start:stop])['Template_error_status']

        return template_error_status

    # This information is to be retrieved directly from the switch (using switch management IP address). Not completed.
    def get_connected_lldp_device(self, switch_ip, port_name):
        """
        Identifying which devices is connected to the trunk via LLDP
        https://developer.arubanetworks.com/aruba-aoscx/reference#get_system-interfaces-name-lldp-neighbors
        :param switch_ip: IP address of the switch
        :param port_name: Interface name. Should be alphanumeric and no more than about 8 bytes long.
        May be the same as the port name, for non-bonded ports.
        Must otherwise be unique among the names of ports, interfaces, and bridges on a host.
        :return:
        """
        api_path = f"https://{switch_ip}/rest/v10.04/system/interfaces/{port_name}/lldp_neighbors"
        headers = {"Accept": "application/json"}
        response = requests.request("GET", api_path, headers=headers)

        return response.text

    # Unable to test without SSID being broadcasted
    def get_ssid_broadcasted(self):
        """
        Which SSID are being broadcasted.
        https://developer.arubanetworks.com/aruba-central/reference/ssids-2
        :return:
        """
        #
        api_path = "/rapids/v1/ssid_allow"
        api_method = "GET"
        api_params = {
            "limit": 20,
            "offset": 0
        }

        response = self.central.command(apiMethod=api_method,
                                    apiPath=api_path,
                                    apiParams=api_params)
        return response

    # Test method
    def _test(self):
        """
        Test API call.
        :return: Sample response: {'code': 200, 'msg': {'data': [['Access Switches'],
        ['Core Switches'], ['default'], ['unprovisioned']], 'total': 4}}
        """
        api_path = "/configuration/v2/groups"
        api_method = "GET"
        api_params = {
            "limit": 20,
            "offset": 0
        }

        response = self.central.command(apiMethod=api_method,
                                    apiPath=api_path,
                                    apiParams=api_params)
        return response

    # Test method
    def _test_networks(self):
        """
        Test API call.
        :return: Sample response: {'code': 200, 'msg': {'data': [['Access Switches'],
        ['Core Switches'], ['default'], ['unprovisioned']], 'total': 4}}
        """
        api_path = "/monitoring/v2/networks"
        api_method = "GET"
        api_params = {
            "limit": 20,
            "offset": 0
        }

        response = self.central.command(apiMethod=api_method,
                                    apiPath=api_path,
                                    apiParams=api_params)
        return response


central_info = {
    "base_url": "https://apigw-apacsouth.central.arubanetworks.com",
    "token": {
        "access_token": "PLEASE_PASTE_HERE"
    }
}


# Tests
a = ArubaCentral(central_info)
sn = "SERIAL_NUMBER"

# Tested - passed
# print(a.get_template(sn))
# print(a.get_template_sync_status(sn))

# TODO: Pending testing
# print(a.get_ap_status(sn))
# print(a.get_ssid_broadcasted())

# Failed tests
# print(a.get_template_info(sn))
# Output: {'code': 500, 'msg': {'description': 'Internal Server Error', 'error_code': '0001', 'service_name': 'Configuration'}}
# Presumably because the configuration is not in place

# Test methods
print(a._test())
print(a._test_networks())