from ..base import DataFrame, MermaidBase, requires_token


class BenthicLIT(MermaidBase):
    """
    A class for handling Benthic Line Intercept Transect (LIT) data from MERMAID.

    The BenthicLIT class is responsible for fetching Benthic LIT data, including observations,
    observations aggregated by sample units, and observations aggregated by sample events,
    for a specified project.
    """

    @requires_token
    def observations(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's Benthic LIT observations.

        Args:
            project_id (str): The ID of the project for which to fetch Benthic LIT observations.

        Returns:
            DataFrame
        """
        url = f"/projects/{project_id}/benthiclits/obstransectbenthiclits/"
        return self.data_frame_from_url(url)

    @requires_token
    def sample_units(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's Benthic LIT observations aggregated by sample units.

        Args:
            project_id (str): The ID of the project for which to fetch Benthic LIT sample units.

        Returns:
            DataFrame
        """

        url = f"/projects/{project_id}/benthiclits/sampleunits/"
        return self.data_frame_from_url(url)

    @requires_token
    def sample_events(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's Benthic LIT observations aggregated by sample events.

        Args:
            project_id (str): The ID of the project for which to fetch Benthic LIT sample events.

        Returns:
            DataFrame
        """
        url = f"/projects/{project_id}/benthiclits/sampleevents/"
        return self.data_frame_from_url(url)
