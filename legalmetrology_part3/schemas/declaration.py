# schemas/declaration.py
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List
from schemas.ocr_region import BoundingBox

class DeclarationField(str, Enum):
    MRP                  = "mrp"
    NET_QUANTITY         = "net_quantity"
    MANUFACTURER_NAME    = "manufacturer_name"
    MANUFACTURER_ADDRESS = "manufacturer_address"
    PACKER_NAME          = "packer_name"
    PACKER_ADDRESS       = "packer_address"
    IMPORTER_NAME        = "importer_name"
    IMPORTER_ADDRESS     = "importer_address"
    COUNTRY_OF_ORIGIN    = "country_of_origin"
    MANUFACTURE_DATE     = "manufacture_date"
    EXPIRY_DATE          = "expiry_date"
    BEST_BEFORE          = "best_before"
    BATCH_NUMBER         = "batch_number"
    CONSUMER_CARE        = "consumer_care"
    LICENSE_NUMBER       = "license_number"
    INGREDIENTS          = "ingredients"
    NUTRITIONAL_INFO     = "nutritional_info"
    GENERIC_NAME         = "generic_name"
    COMMODITY_NAME       = "commodity_name"
    UNKNOWN              = "unknown"

@dataclass
class ExtractedDeclaration:
    field: DeclarationField
    raw_text: str
    normalized_value: Optional[str]
    source_region_ids: List[str]
    classifier_confidence: float
    font_size_pt: Optional[float]
    bounding_box: Optional[BoundingBox]
    language: Optional[str]