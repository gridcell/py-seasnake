from ..base import MermaidBase, pd, requires_token


class BenthicPIT(MermaidBase):
    """
    A class for handling Benthic Point Intercept Transect (PIT) data from MERMAID.

    The BenthicPIT class is responsible for fetching Benthic PIT data, including observations,
    observations aggregated by sample units, and observations aggregated by sample events,
    for a specified project.
    """

    @requires_token
    def observations(self, project_id: str) -> pd.DataFrame:
        """
        Retrieves a project's Benthic PIT observations.

        Args:
            project_id (str): The ID of the project for which to fetch Benthic PIT observations.

        Returns:
            pd.DataFrame
        """
        url = f"/projects/{project_id}/benthicpits/obstransectbenthicpits/"
        return self.data_frame_from_url(url)

    @requires_token
    def sample_units(self, project_id: str) -> pd.DataFrame:
        """
        Retrieves a project's Benthic PIT observations aggregated by sample units.

        Args:
            project_id (str): The ID of the project for which to fetch Benthic PIT sample units.

        Returns:
            pd.DataFrame
        """
        url = f"/projects/{project_id}/benthicpits/sampleunits/"
        return self.data_frame_from_url(url)

    @requires_token
    def sample_events(self, project_id: str) -> pd.DataFrame:
        """
        Retrieves a project's Benthic PIT observations aggregated by sample events.

        Args:
            project_id (str): The ID of the project for which to fetch Benthic PIT sample events.

        Returns:
            pd.DataFrame
        """
        url = f"/projects/{project_id}/benthicpits/sampleevents/"
        return self.data_frame_from_url(url)
