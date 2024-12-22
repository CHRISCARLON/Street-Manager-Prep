{% set table_alias = 'usrn_permit_details_london_latest' %}
{{ config(materialized='table', alias=table_alias) }}

WITH combined_permits AS (
    SELECT 
        usrn,
        street_name,
        highway_authority,
        permit_reference_number,
        promoter_organisation,
        work_category,
        activity_type,
        is_ttro_required,
        is_traffic_sensitive,
        traffic_management_type_ref,
        ofgem_electricity_licence,
        ofgem_gas_licence,
        ofcom_licence,
        ofwat_licence
    FROM {{ ref('in_progress_list_london') }}
    
    UNION ALL
    
    SELECT 
        usrn,
        street_name,
        highway_authority,
        permit_reference_number,
        promoter_organisation,
        work_category,
        activity_type,
        is_ttro_required,
        is_traffic_sensitive,
        traffic_management_type_ref,
        ofgem_electricity_licence,
        ofgem_gas_licence,
        ofcom_licence,
        ofwat_licence
    FROM {{ ref('completed_list_london') }}
)

SELECT 
    *,
    {{ current_timestamp() }} AS date_processed
FROM combined_permits