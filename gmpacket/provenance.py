from typing import Dict

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class Website(BaseModel):
    """Represent a ground motion packet Website object."""

    url: str = Field(alias="$")
    site_type: str = Field(alias="type", default="xsd:anyURI")

    model_config: ConfigDict = ConfigDict(populate_by_name=True)


class OrganizationAgent(BaseModel):
    """Represent a ground motion packet OrganizationAgent object."""

    label: str = Field(alias="prov:label", default=None)
    type: Dict = Field(
        alias="prov:type",
        default={"$": "prov:Organization", "type": "prov:QUALIFIED_NAME"},
    )
    name: str = Field(alias="seis_prov:name")
    role: str = Field(alias="seis_prov:role")
    website: Website = Field(alias="seis_prov:website")

    model_config: ConfigDict = ConfigDict(populate_by_name=True)

    @classmethod
    def from_params(cls, name: str, role: str, website: Website, label: str = None):
        if label is None:
            label = name
        thisobj = cls(label=label, name=name, role=role, website=website)
        return thisobj


class SoftwareAgent(BaseModel):
    """Represent a ground motion packet SoftwareAgent object."""

    label: str = Field(alias="prov:label", default=None)
    type: Dict = Field(
        alias="prov:type",
        default={"$": "prov:SoftwareAgent", "type": "prov:QUALIFIED_NAME"},
    )
    name: str = Field(alias="seis_prov:software_name")
    version: str = Field(alias="seis_prov:software_version")
    website: Website = Field(alias="seis_prov:website")

    model_config: ConfigDict = ConfigDict(populate_by_name=True)

    @classmethod
    def from_params(cls, name: str, version: str, website: Website, label: str = None):
        if label is None:
            label = name
        thisobj = cls(label=label, name=name, version=version, website=website)
        return thisobj


class PersonAgent(BaseModel):
    """Represent a ground motion packet PersonAgent object."""

    label: str = Field(alias="prov:label")
    type: Dict = Field(
        alias="prov:type", default={"$": "prov:Person", "type": "prov:QUALIFIED_NAME"}
    )
    name: str = Field(alias="seis_prov:name")
    email: EmailStr = Field(alias="seis_prov:email")
    role: str = Field(alias="seis_prov:role")

    model_config: ConfigDict = ConfigDict(populate_by_name=True)

    @classmethod
    def from_params(cls, name: str, email: str, role: str, label: str = None):
        if label is None:
            label = name
        thisobj = cls(label=label, name=name, email=email, role=role)
        return thisobj


class Provenance(BaseModel):
    """Represent a ground motion packet Provenance object."""

    prefix: dict = {"seis_prov": "http://seisprov.org/seis_prov/0.1/#"}
    # agent: Optional[Dict[str, Agent]]
    agent: dict

    @field_validator("agent")
    def get_agent_dict(cls, input):
        """Check elements of input dictionary to make sure they are all *Agent types"""
        if not isinstance(input, dict):
            raise ValueError("agent attribute of Provenance must be a dictionary.")
        agents = {}
        agent_types = (OrganizationAgent, SoftwareAgent, PersonAgent)
        for key, value in input.items():
            if isinstance(value, dict):
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
                        raise ValueError(
                            f"Incorrectly designated PersonAgent: '{str(e)}'."
                        )
                elif agent_type == "prov:Organization":
                    try:
                        agent = OrganizationAgent(**value)
                    except Exception as e:
                        raise ValueError(
                            f"Incorrectly designated OrganizationAgent: '{str(e)}'."
                        )
                agents[key] = agent
            elif isinstance(value, agent_types):
                agents[key] = value
            else:
                raise ValueError(f"Unknown agent type {agent_type}.")

        return agents

    def getAgents(self):
        return list(self.agent.keys())
