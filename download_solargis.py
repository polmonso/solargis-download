import requests
import logging
import xmlschema

from typing import NamedTuple, Dict

import datetime

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

#https://github.com/Som-Energia/plantmonitor/blob/master/external_api/api_solargis.py#L243


class PVSystem(NamedTuple):
    geometry_type: str
    geometry_azimuth: int
    geometry_tilt: int
    geometry_backTracking: bool
    geometry_rotationLimitEast: int
    geometry_rotationLimitWest: int
    system_installedPower: int # TO BE DELETED
    system_installationType: str # TO BE DELETED
    system_dateStartup: str
    system_selfShading: bool
    module_type: str
    degradation_content: float
    degradationFirstYear_content: float
    PmaxCoeff_content: float
    efficiency_type: str
    efficiency_content: float
    limitationACPower_content: int
    dcLosses_snowPollution: float
    dcLosses_cables: float
    dcLosses_mismatch: float
    acLosses_transformer: float
    acLosses_cables: float
    topology_xsi_type: str
    topology_relativeSpacing: float
    topology_type: str

class Site(NamedTuple):
    id: int
    name: str
    peak_power_w: int
    latitude: float
    longitude: float
    installation_type: str
    pvsystem: PVSystem

def get_payload():
    
    
    pvsystem = PVSystem(
        geometry_type='GeometryFixedOneAngle',
        geometry_azimuth=172,
        geometry_tilt=25,
        geometry_backTracking=None,
        geometry_rotationLimitEast=None,
        geometry_rotationLimitWest=None,
        system_installedPower=841,
        system_installationType='FREE_STANDING',
        system_dateStartup='2020-10-14',
        system_selfShading='true',
        module_type='CSI',
        degradation_content=0.7,
        degradationFirstYear_content=2.50,
        PmaxCoeff_content=-0.4,
        efficiency_type='EfficiencyConstant',
        efficiency_content=98.3,
        limitationACPower_content=720,
        dcLosses_snowPollution=2.00,
        dcLosses_cables=1.0,
        dcLosses_mismatch=0.25,
        acLosses_transformer=0.50,
        acLosses_cables=0.25,
        topology_xsi_type='TopologyRow',
        topology_relativeSpacing=2.5,
        topology_type='UNPROPORTIONAL1',
    )
    
    
    return f'''
    <ws:dataDeliveryRequest dateFrom="2023-01-01" dateTo="2023-01-15"
            xmlns="http://geomodel.eu/schema/data/request"
            xmlns:ws="http://geomodel.eu/schema/ws/data"
            xmlns:geo="http://geomodel.eu/schema/common/geo"
            xmlns:pv="http://geomodel.eu/schema/common/pv"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <site id="Terborg" lat="37.236035" lng="-2.296076">
                <pv:geometry xsi:type="pv:{pvsystem.geometry_type}" azimuth="{pvsystem.geometry_azimuth}" tilt="{pvsystem.geometry_tilt}"/>
                <pv:system installedPower="841" installationType="FREE_STANDING" dateStartup="{pvsystem.system_dateStartup}" selfShading="{pvsystem.system_selfShading}">
                    <pv:module type="{pvsystem.module_type}">
                        <pv:degradation>{pvsystem.degradation_content}</pv:degradation>
                        <pv:degradationFirstYear>{pvsystem.degradationFirstYear_content}</pv:degradationFirstYear>
                        <pv:PmaxCoeff>{pvsystem.PmaxCoeff_content}</pv:PmaxCoeff>
                    </pv:module>
                    <pv:inverter>
                        <pv:efficiency xsi:type="pv:{pvsystem.efficiency_type}" percent="{pvsystem.efficiency_content}"/>
                        <pv:limitationACPower>{pvsystem.limitationACPower_content}</pv:limitationACPower>
                    </pv:inverter>
                    <pv:losses>
                        <pv:acLosses cables="{pvsystem.acLosses_cables}" transformer="{pvsystem.acLosses_transformer}"/>
                        <pv:dcLosses cables="{pvsystem.dcLosses_cables}" mismatch="{pvsystem.dcLosses_mismatch}" snowPollution="{pvsystem.dcLosses_snowPollution}"/>
                    </pv:losses>
                <pv:topology xsi:type="pv:{pvsystem.topology_xsi_type}" relativeSpacing="{pvsystem.topology_relativeSpacing}" type="{pvsystem.topology_type}"/>
                </pv:system>
            </site>
            <processing key="GTI TMOD PVOUT" summarization="HOURLY" terrainShading="true">
            </processing>
    </ws:dataDeliveryRequest>
    '''

def rfc3336todt(datetimestr):
    return datetime.datetime.strptime(datetimestr, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=datetime.timezone.utc)

def text_response_to_readings(text_response, request_time=None):

    schema = xmlschema.XMLSchema('ws-data.xsd')

    request_time = request_time or datetime.datetime.now(datetime.timezone.utc)

    response_dict = schema.to_dict(text_response)
    readings_dirty = response_dict['site'][0]['row']
    readings = [
        (rfc3336todt(v['@dateTime']), *v['@values'])
        for v in readings_dirty
    ]
    return readings

def get_arbitrary_payload():
    headers = {'Content-Type' : 'application/xml'}

    xml_request_content = get_payload()

    from env import SOLARGIS

    try:
        response = requests.post(
            f"{SOLARGIS['api_base_url']}/datadelivery/request",
            params={'key':SOLARGIS['api_key']},
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
    else:
        text_response = response.text
        readings = text_response_to_readings(text_response)
    
    return response.status_code, readings

if __name__ == '__main__':
    status, results = get_arbitrary_payload()

    
    [print(f'{result[0].isoformat()},{result[1]},{result[2]},{result[3]}') for result in results]
    foo = [f'{result[0].isoformat()},{result[1]},{result[2]},{result[3]}' for result in results]
    with open('solargis.csv', 'w') as opened_file:
        opened_file.write('\n'.join(foo))
    


