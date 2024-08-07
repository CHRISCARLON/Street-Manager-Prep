# unit_test/test_street_manager_flatten_json.py

from src.street_manager.extract_load_data import flatten_json

def test_flatten_json():
    # Test case 1: Nested JSON object with the provided test data
    json_data = {
        "event_reference": 529770,
        "event_type": "work-start",
        "object_data": {
            "work_reference_number": "TSR1591199404915",
            "permit_reference_number": "TSR1591199404915-01",
            "promoter_swa_code": "STPR",
            "promoter_organisation": "Smoke Test Promoter",
            "highway_authority": "CITY OF WESTMINSTER",
            "works_location_coordinates": "LINESTRING(501251.53 222574.64,501305.92 222506.65)",
            "street_name": "HIGH STREET NORTH",
            "area_name": "LONDON",
            "work_category": "Standard",
            "traffic_management_type": "Road closure",
            "proposed_start_date": "2020-06-10T00:00:00.000Z",
            "proposed_start_time": "2020-06-10T13:50:00.000Z",
            "proposed_end_date": "2020-06-12T00:00:00.000Z",
            "proposed_end_time": None,
            "actual_start_date_time": "2020-06-11T10:11:00.000Z",
            "actual_end_date_time": None,
            "work_status": "Works in progress",
            "usrn": "8401426",
            "highway_authority_swa_code": "5990",
            "work_category_ref": "standard",
            "traffic_management_type_ref": "road_closure",
            "work_status_ref": "in_progress",
            "activity_type": "Remedial works",
            "is_ttro_required": "No",
            "is_covid_19_response": "No",
            "works_location_type": "Cycleway, Footpath",
            "permit_conditions": "NCT01a, NCT01b, NCT11a",
            "road_category": "3",
            "is_traffic_sensitive": "Yes",
            "is_deemed": "No",
            "permit_status": "permit_modification_request",
            "town": "LONDON",
            "collaborative_working": "Yes",
            "collaboration_type": "Other",
            "collaboration_type_ref": "other",
            "close_footway": "Yes, a pedestrian walkway will be provided",
            "close_footway_ref": "yes_provide_pedestrian_walkway",
            "current_traffic_management_type": "Multi-way signals",
            "current_traffic_management_type_ref": "multi_way_signals",
            "current_traffic_management_update_date": "2020-06-11T10:11:00.000Z"
        },
        "event_time": "2020-06-04T08:00:00.000Z",
        "object_type": "PERMIT",
        "object_reference": "TSR1591199404915-01",
        "version": 1
    }
    expected_output = {
        "event_reference": 529770,
        "event_type": "work-start",
        "object_data.work_reference_number": "TSR1591199404915",
        "object_data.permit_reference_number": "TSR1591199404915-01",
        "object_data.promoter_swa_code": "STPR",
        "object_data.promoter_organisation": "Smoke Test Promoter",
        "object_data.highway_authority": "CITY OF WESTMINSTER",
        "object_data.works_location_coordinates": "LINESTRING(501251.53 222574.64,501305.92 222506.65)",
        "object_data.street_name": "HIGH STREET NORTH",
        "object_data.area_name": "LONDON",
        "object_data.work_category": "Standard",
        "object_data.traffic_management_type": "Road closure",
        "object_data.proposed_start_date": "2020-06-10T00:00:00.000Z",
        "object_data.proposed_start_time": "2020-06-10T13:50:00.000Z",
        "object_data.proposed_end_date": "2020-06-12T00:00:00.000Z",
        "object_data.proposed_end_time": None,
        "object_data.actual_start_date_time": "2020-06-11T10:11:00.000Z",
        "object_data.actual_end_date_time": None,
        "object_data.work_status": "Works in progress",
        "object_data.usrn": "8401426",
        "object_data.highway_authority_swa_code": "5990",
        "object_data.work_category_ref": "standard",
        "object_data.traffic_management_type_ref": "road_closure",
        "object_data.work_status_ref": "in_progress",
        "object_data.activity_type": "Remedial works",
        "object_data.is_ttro_required": "No",
        "object_data.is_covid_19_response": "No",
        "object_data.works_location_type": "Cycleway, Footpath",
        "object_data.permit_conditions": "NCT01a, NCT01b, NCT11a",
        "object_data.road_category": "3",
        "object_data.is_traffic_sensitive": "Yes",
        "object_data.is_deemed": "No",
        "object_data.permit_status": "permit_modification_request",
        "object_data.town": "LONDON",
        "object_data.collaborative_working": "Yes",
        "object_data.collaboration_type": "Other",
        "object_data.collaboration_type_ref": "other",
        "object_data.close_footway": "Yes, a pedestrian walkway will be provided",
        "object_data.close_footway_ref": "yes_provide_pedestrian_walkway",
        "object_data.current_traffic_management_type": "Multi-way signals",
        "object_data.current_traffic_management_type_ref": "multi_way_signals",
        "object_data.current_traffic_management_update_date": "2020-06-11T10:11:00.000Z",
        "event_time": "2020-06-04T08:00:00.000Z",
        "object_type": "PERMIT",
        "object_reference": "TSR1591199404915-01",
        "version": 1
    }
    assert flatten_json(json_data) == expected_output