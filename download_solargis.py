import requests
import logging

def get_payload_original():
    return f'''
    <ws:dataDeliveryRequest dateFrom="{from_date_str}" dateTo="{to_date_str}"
            xmlns="http://geomodel.eu/schema/data/request"
            xmlns:ws="http://geomodel.eu/schema/ws/data"
            xmlns:geo="http://geomodel.eu/schema/common/geo"
            xmlns:pv="http://geomodel.eu/schema/common/pv"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <site id="{site.name}" lat="{site.latitude}" lng="{site.longitude}">
                <pv:geometry xsi:type="pv:{site.pvsystem.geometry_type}" azimuth="{site.pvsystem.geometry_azimuth}" tilt="{site.pvsystem.geometry_tilt}"/>
                <pv:system installedPower="{site.peak_power_w}" installationType="{site.installation_type}" dateStartup="{site.pvsystem.system_dateStartup}" selfShading="{site.pvsystem.system_selfShading}">
                    <pv:module type="{site.pvsystem.module_type}">
                        <pv:degradation>{site.pvsystem.degradation_content}</pv:degradation>
                        <pv:degradationFirstYear>{site.pvsystem.degradationFirstYear_content}</pv:degradationFirstYear>
                        <pv:PmaxCoeff>{site.pvsystem.PmaxCoeff_content}</pv:PmaxCoeff>
                    </pv:module>
                    <pv:inverter>
                        <pv:efficiency xsi:type="pv:{site.pvsystem.efficiency_type}" percent="{site.pvsystem.efficiency_content}"/>
                        <pv:limitationACPower>{site.pvsystem.limitationACPower_content}</pv:limitationACPower>
                    </pv:inverter>
                    <pv:losses>
                        <pv:acLosses cables="{site.pvsystem.acLosses_cables}" transformer="{site.pvsystem.acLosses_transformer}"/>
                        <pv:dcLosses cables="{site.pvsystem.dcLosses_cables}" mismatch="{site.pvsystem.dcLosses_mismatch}" snowPollution="{site.pvsystem.dcLosses_snowPollution}"/>
                    </pv:losses>
                <pv:topology xsi:type="pv:{site.pvsystem.topology_xsi_type}" relativeSpacing="{site.pvsystem.topology_relativeSpacing}" type="{site.pvsystem.topology_type}"/>
                </pv:system>
            </site>
            <processing key="{processing_keys}" summarization="HOURLY" terrainShading="true">
            </processing>
    </ws:dataDeliveryRequest>
    '''

def get_payload():
    return f'''
    <ws:dataDeliveryRequest dateFrom="{from_date_str}" dateTo="{to_date_str}"
            xmlns="http://geomodel.eu/schema/data/request"
            xmlns:ws="http://geomodel.eu/schema/ws/data"
            xmlns:geo="http://geomodel.eu/schema/common/geo"
            xmlns:pv="http://geomodel.eu/schema/common/pv"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <site id="{site.name}" lat="{site.latitude}" lng="{site.longitude}">
                <pv:geometry xsi:type="pv:{site.pvsystem.geometry_type}" azimuth="{site.pvsystem.geometry_azimuth}" tilt="{site.pvsystem.geometry_tilt}"/>
                <pv:system installedPower="{site.peak_power_w}" installationType="{site.installation_type}" dateStartup="{site.pvsystem.system_dateStartup}" selfShading="{site.pvsystem.system_selfShading}">
                    <pv:module type="{site.pvsystem.module_type}">
                        <pv:degradation>{site.pvsystem.degradation_content}</pv:degradation>
                        <pv:degradationFirstYear>{site.pvsystem.degradationFirstYear_content}</pv:degradationFirstYear>
                        <pv:PmaxCoeff>{site.pvsystem.PmaxCoeff_content}</pv:PmaxCoeff>
                    </pv:module>
                    <pv:inverter>
                        <pv:efficiency xsi:type="pv:{site.pvsystem.efficiency_type}" percent="{site.pvsystem.efficiency_content}"/>
                        <pv:limitationACPower>{site.pvsystem.limitationACPower_content}</pv:limitationACPower>
                    </pv:inverter>
                    <pv:losses>
                        <pv:acLosses cables="{site.pvsystem.acLosses_cables}" transformer="{site.pvsystem.acLosses_transformer}"/>
                        <pv:dcLosses cables="{site.pvsystem.dcLosses_cables}" mismatch="{site.pvsystem.dcLosses_mismatch}" snowPollution="{site.pvsystem.dcLosses_snowPollution}"/>
                    </pv:losses>
                <pv:topology xsi:type="pv:{site.pvsystem.topology_xsi_type}" relativeSpacing="{site.pvsystem.topology_relativeSpacing}" type="{site.pvsystem.topology_type}"/>
                </pv:system>
            </site>
            <processing key="{processing_keys}" summarization="HOURLY" terrainShading="true">
            </processing>
    </ws:dataDeliveryRequest>
    '''

def get_arbitrary_payload():
        headers = {'Content-Type' : 'application/xml'}

        xml_request_content = get_payload()

        from env import SOLARGIS

        try:
            response = requests.post(
                SOLARGIS['api_base_url'],
                params=SOLARGIS['api_key'],
                headers=headers,
                data=xml_request_content.encode('utf8'),
                timeout=30
            )
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error("Request exception {} msg: {}".format(e, response.text))
            return response.status_code, None

        if response.status_code != 200:
            logging.error("Request error {}".format(response.text))

        text_response = response.text
        return response.status_code, text_response

if __name__ == '__main__':
    results = get_arbitrary_payload()

    logging.info(results)



