import os
import tempfile
import zipfile
import requests
import pandas as pd
import fiona

from shapely import wkt
from shapely.geometry import shape
from loguru import logger

from .process_into_motherduck import process_chunk


def load_geopackage_open_usrns(url, conn, limit):
    """
    Function to load OS open usrn data in batches of 50,000 rows.

    It taskes a duckdb connection object and the download url required.

    Args:
        Url for data
        Connection object
    """

    # This can be changed based on how much memory you want to use overall
    chunk_size = limit

    # List to store errors
    errors = []

    try:
        # Download the zip file
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Write the zip file to the temporary directory
            zip_path = os.path.join(temp_dir, 'temp.zip')
            with open(zip_path, 'wb') as zip_file:
                zip_file.write(response.content)

            # Extract the contents of the zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # Find the GeoPackage file
            gpkg_file = None
            for file_name in os.listdir(temp_dir):
                if file_name.endswith('.gpkg'):
                    gpkg_file = os.path.join(temp_dir, file_name)
                    break

            if gpkg_file:
                try:
                    # Open the GeoPackage file
                    with fiona.open(gpkg_file, 'r') as src:
                        # Print some of the metadata to check everything is OK
                        crs = src.crs
                        schema = src.schema

                        logger.info(f"The CRS is: {crs}")
                        logger.info(f"The Schema is: {schema}")

                        # List to store extracted features for DataFrame processing
                        features = []

                        for i, feature in enumerate(src):
                            try:
                                # Convert geometry to WKT string
                                geom = shape(feature['geometry'])
                                feature['properties']['geometry'] = wkt.dumps(geom)
                            except Exception as e:
                                # If there's an error converting the geometry, set it to None
                                # and log the index of the feature that failed so we're aware of what features failed
                                # This could be made better - could we store these errors somewhere for future use?
                                feature['properties']['geometry'] = None
                                error_msg = f"Error converting geometry for feature {i}: {e}"
                                logger.warning(error_msg)
                                errors.append(error_msg)

                            # Append each feature to the list
                            features.append(feature['properties'])

                            # When the list hits the limit size - e.g. 75,000
                            # Process list into DataFrame
                            if len(features) == chunk_size:
                                # Process the chunk
                                df_chunk = pd.DataFrame(features)
                                process_chunk(df_chunk, conn)
                                logger.info(f"Processed features {i-chunk_size+1} to {i}")

                                # Empty the list
                                features = []

                        # Process any remaining features outside the loop
                        if features:
                            df_chunk = pd.DataFrame(features)
                            process_chunk(df_chunk, conn)
                            logger.info("Processed remaining features")
                            # Empty the list
                            features = []

                except Exception as e:
                    error_msg = f"Error processing GeoPackage: {e}"
                    logger.error(error_msg)
                    errors.append(error_msg)
                    raise
            else:
                error_msg = "No GeoPackage file found in the zip archive"
                logger.error(error_msg)
                errors.append(error_msg)
                raise FileNotFoundError(error_msg)
    except Exception as e:
        error_msg = f"Error processing the zip file: {e}"
        logger.error(error_msg)
        errors.append(error_msg)
        raise
    finally:
        # Print all errors + total amount of errors
        if errors:
            logger.error(f"Total errors encountered: {len(errors)}")
            for error in errors:
                print(error)
    return None
