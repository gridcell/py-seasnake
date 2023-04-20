from ..base import MermaidBase, pd, requires_token


class BenthicPhotoQuadrat(MermaidBase):
    """
    A class for handling Benthic Photo Quadrat data from MERMAID.

    The BenthicPhotoQuadrat class is responsible for fetching Benthic Photo Quadrat data,
    including observations, observations aggregated by sample units, and observations
    aggregated by sample events, for a specified project.
    """

    @requires_token
    def observations(self, project_id: str) -> pd.DataFrame:
        """
        Retrieves a project's Benthic Photo Quadrat observations.

        Args:
            project_id (str): The ID of the project for which to fetch
            Benthic Photo Quadrat observations.

        Returns:
            pd.DataFrame
        """
        url = f"/projects/{project_id}/benthicpqts/obstransectbenthicpqts/"
        return self.data_frame_from_url(url)

    @requires_token
    def sample_units(self, project_id: str) -> pd.DataFrame:
        """
        Retrieves a project's Benthic Photo Quadrat observations aggregated by sample units.

        Args:
            project_id (str): The ID of the project for which to fetch
            Benthic Photo Quadrat sample units.

        Returns:
            pd.DataFrame
        """
        url = f"/projects/{project_id}/benthicpqts/sampleunits/"
        return self.data_frame_from_url(url)

    @requires_token
    def sample_events(self, project_id: str) -> pd.DataFrame:
        """
        Retrieves a project's Benthic Photo Quadrat observations aggregated by sample events.

        Args:
            project_id (str): The ID of the project for which to fetch
            Benthic Photo Quadrat sample events.

        Returns:
            pd.DataFrame
        """
        url = f"/projects/{project_id}/benthicpqts/sampleevents/"
        return self.data_frame_from_url(url)
