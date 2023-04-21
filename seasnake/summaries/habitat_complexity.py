from ..base import DataFrame, MermaidBase, requires_token


class HabitatComplexity(MermaidBase):
    """
    A class for handling habitat complexity data from MERMAID.

    The HabitatComplexity class is responsible for fetching habitat complexity
    data, including observations, observations aggregated by sample units, and
    observations aggregated by sample events, for a specified project.
    """

    @requires_token
    def observations(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's habitat complexity observations.

        Args:
            project_id (str): The ID of the project for which to fetch
            habitat complexity observations.

        Returns:
            DataFrame
        """
        url = f"/projects/{project_id}/habitatcomplexities/obshabitatcomplexities/"
        return self.data_frame_from_url(url)

    @requires_token
    def sample_units(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's habitat complexity observations aggregated by sample units.

        Args:
            project_id (str): The ID of the project for which to fetch
            habitat complexity sample units.

        Returns:
            DataFrame
        """
        url = f"/projects/{project_id}/habitatcomplexities/sampleunits/"
        return self.data_frame_from_url(url)

    @requires_token
    def sample_events(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's habitat complexity observations aggregated by sample events.

        Args:
            project_id (str): The ID of the project for which to fetch
            habitat complexity sample events.

        Returns:
            DataFrame
        """
        url = f"/projects/{project_id}/habitatcomplexities/sampleevents/"
        return self.data_frame_from_url(url)
