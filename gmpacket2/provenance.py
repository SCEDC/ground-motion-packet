from typing import Dict

from pydantic import BaseModel, EmailStr, Field, root_validator, validator


class Website(BaseModel):
    url: str = Field(alias="$")
    site_type: str = Field(alias="type", default="xsd:anyURI")

    class Config:
        allow_population_by_field_name = True


class OrganizationAgent(BaseModel):
    label: str = Field(alias="prov:label", default=None)
    prov_type: Dict = Field(
        alias="prov:type",
        default={"$": "prov:Organization", "type": "prov:QUALIFIED_NAME"},
    )
    name: str = Field(alias="seis_prov:name")
    role: str = Field(alias="seis_prov:role")
    website: Website = Field(alias="seis_prov:website")

    class Config:
        allow_population_by_field_name = True

    @root_validator(pre=True)
    def set_label(cls, values):
        if "label" not in values and "prov:label" not in values:
            values["label"] = values["name"]
        return values


class SoftwareAgent(BaseModel):
    label: str = Field(alias="prov:label", default=None)
    prov_type: Dict = Field(
        alias="prov:type",
        default={"$": "prov:SoftwareAgent", "type": "prov:QUALIFIED_NAME"},
    )
    name: str = Field(alias="seis_prov:software_name")
    version: str = Field(alias="seis_prov:software_version")
    website: Website = Field(alias="seis_prov:website")

    class Config:
        allow_population_by_field_name = True

    @root_validator(pre=True)
    def set_label(cls, values):
        if "label" not in values and "prov:label" not in values:
            values["label"] = values["name"]
        return values


class PersonAgent(BaseModel):
    label: str = Field(alias="prov:label")
    prov_type: Dict = Field(
        alias="prov:type", default={"$": "prov:Person", "type": "prov:QUALIFIED_NAME"}
    )
    name: str = Field(alias="seis_prov:name")
    email: EmailStr = Field(alias="seis_prov:email")
    role: str = Field(alias="seis_prov:role")

    class Config:
        allow_population_by_field_name = True

    @root_validator(pre=True)
    def set_label(cls, values):
        if "label" not in values and "prov:label" not in values:
            values["label"] = values["name"]
        return values


class Provenance(BaseModel):
    prefix = {"seis_prov": "http://seisprov.org/seis_prov/0.1/#"}
    # agent: Optional[Dict[str, Agent]]
    agent: dict

    @validator("agent")
    def get_agent_dict(cls, input):
        if not isinstance(input, dict):
            raise ValueError("agent attribute of Provenance must be a dictionary.")
        agents = {}
        for key, value in input.items():
            if "prov:type" not in value:
                raise ValueError("Agent missing 'prov:type' attribute.")
            agent_type = value["prov:type"]["$"]
            if agent_type == "prov:SoftwareAgent":
                try:
                    agent = SoftwareAgent(**value)
                except Exception as e:
                    raise ValueError(
                        f"Incorrectly designated SoftwareAgent: '{str(e)}'."
                    )
            elif agent_type == "prov:Person":
                try:
                    agent = PersonAgent(**value)
                except Exception as e:
                    raise ValueError(f"Incorrectly designated PersonAgent: '{str(e)}'.")
            elif agent_type == "prov:Organization":
                try:
                    agent = OrganizationAgent(**value)
                except Exception as e:
                    raise ValueError(
                        f"Incorrectly designated OrganizationAgent: '{str(e)}'."
                    )
            else:
                raise ValueError(f"Unknown agent type {agent_type}.")
            agents[key] = agent
        return agents
