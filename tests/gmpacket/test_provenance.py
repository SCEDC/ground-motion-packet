import json
from datetime import datetime
from typing import Dict, List, Optional

from deepdiff import DeepDiff
from pydantic import BaseModel, EmailStr, Field, root_validator, validator

from gmpacket.provenance import (
    OrganizationAgent,
    PersonAgent,
    Provenance,
    SoftwareAgent,
    Website,
)
from test_utils import get_jdict


def test_software_agent():
    jdict = get_jdict()
    data = jdict["provenance"]["agent"]["seis_prov:sp000_sa_0000000"]
    software = SoftwareAgent(**data)
    assert software.dict(by_alias=True) == data


def test_person_agent():
    jdict = get_jdict()
    data = jdict["provenance"]["agent"]["seis_prov:sp000_pp_0000000"]
    person = PersonAgent(**data)
    assert person.dict(by_alias=True) == data


def test_organization_agent():
    jdict = get_jdict()
    data = jdict["provenance"]["agent"]["seis_prov:sp000_og_0000000"]
    organization = OrganizationAgent(**data)
    assert organization.dict(by_alias=True) == data


def test_website():
    jdict = get_jdict()
    data = jdict["provenance"]["agent"]["seis_prov:sp000_og_0000000"][
        "seis_prov:website"
    ]
    website = Website(**data)
    assert website.dict(by_alias=True) == data


def test_provenance():
    jdict = get_jdict()
    data = jdict["provenance"]
    provenance = Provenance(**data)
    assert provenance.dict(by_alias=True) == data


def test_create_objects():
    website = Website(url="www.flintstone.org")

    organization = OrganizationAgent.from_params("flintstones.org", "creator", website)
    cmp_dict = {
        "prov:label": "flintstones.org",
        "prov:type": {"$": "prov:Organization", "type": "prov:QUALIFIED_NAME"},
        "seis_prov:name": "flintstones.org",
        "seis_prov:role": "creator",
        "seis_prov:website": {"$": "www.flintstone.org", "type": "xsd:anyURI"},
    }
    assert organization.dict(by_alias=True) == cmp_dict

    # software = SoftwareAgent(name="gmprocess", version="1.2", website=website)
    software = SoftwareAgent.from_params(
        name="gmprocess", version="1.2", website=website
    )
    cmp_dict = {
        "prov:label": "gmprocess",
        "prov:type": {"$": "prov:SoftwareAgent", "type": "prov:QUALIFIED_NAME"},
        "seis_prov:software_name": "gmprocess",
        "seis_prov:software_version": "1.2",
        "seis_prov:website": {"$": "www.flintstone.org", "type": "xsd:anyURI"},
    }
    assert software.dict(by_alias=True) == cmp_dict

    # person = PersonAgent(name="Fred", email="fred@flintstones.org", role="developer")
    person = PersonAgent.from_params(
        name="Fred", email="fred@flintstones.org", role="developer"
    )
    cmp_dict = {
        "prov:label": "Fred",
        "prov:type": {"$": "prov:Person", "type": "prov:QUALIFIED_NAME"},
        "seis_prov:name": "Fred",
        "seis_prov:email": "fred@flintstones.org",
        "seis_prov:role": "developer",
    }
    assert person.dict(by_alias=True) == cmp_dict

    agents = {"software": software, "person": person, "organization": organization}
    provenance = Provenance(agent=agents)
    cmp_dict = {
        "agent": {
            "software": {
                "prov:label": "gmprocess",
                "seis_prov:software_name": "gmprocess",
                "seis_prov:software_version": "1.2",
                "seis_prov:website": {"$": "www.flintstone.org", "type": "xsd:anyURI"},
                "prov:type": {"$": "prov:SoftwareAgent", "type": "prov:QUALIFIED_NAME"},
            },
            "person": {
                "prov:label": "Fred",
                "seis_prov:name": "Fred",
                "seis_prov:email": "fred@flintstones.org",
                "seis_prov:role": "developer",
                "prov:type": {"$": "prov:Person", "type": "prov:QUALIFIED_NAME"},
            },
            "organization": {
                "prov:label": "flintstones.org",
                "seis_prov:name": "flintstones.org",
                "seis_prov:role": "creator",
                "seis_prov:website": {"$": "www.flintstone.org", "type": "xsd:anyURI"},
                "prov:type": {"$": "prov:Organization", "type": "prov:QUALIFIED_NAME"},
            },
        },
        "prefix": {"seis_prov": "http://seisprov.org/seis_prov/0.1/#"},
    }
    assert cmp_dict == provenance.dict(by_alias=True)


if __name__ == "__main__":
    test_create_objects()
    test_software_agent()
    test_organization_agent()
    test_website()
    test_person_agent()
    test_provenance()
