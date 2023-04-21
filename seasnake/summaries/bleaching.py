from ..base import DataFrame, MermaidBase, requires_token


class Bleaching(MermaidBase):
    """
    A class for handling coral bleaching data from MERMAID.

    The Bleaching class is responsible for fetching bleaching data, including observations,
    observations aggregated by sample units, and observations aggregated by sample events,
    for a specified project.
    """

    @requires_token
    def colonies_bleached_observations(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's Bleaching colonies bleached observations.

        Args:
            project_id (str): The ID of the project for which to fetch Bleaching observations.

        Returns:
            DataFrame
        """
        url = f"/projects/{project_id}/bleachingqcs/obscoloniesbleacheds/"
        return self.data_frame_from_url(url)

    @requires_token
    def percent_cover_observations(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's Bleaching percent cover of hard coral, macroalgae and
        soft coral observations.

        Args:
            project_id (str): The ID of the project for which to fetch Bleaching observations.

        Returns:
            DataFrame
        """
        url = f"/projects/{project_id}/bleachingqcs/obsquadratbenthicpercents/"
        return self.data_frame_from_url(url)

    @requires_token
    def sample_units(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's Bleaching observations aggregated by sample units.

        Args:
            project_id (str): The ID of the project for which to fetch Bleaching sample units.

        Returns:
            DataFrame
        """
        url = f"/projects/{project_id}/bleachingqcs/sampleunits/"
        return self.data_frame_from_url(url)

    @requires_token
    def sample_events(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's Bleaching observations aggregated by sample events.

        Args:
            project_id (str): The ID of the project for which to fetch Bleaching sample events.

        Returns:
            DataFrame
        """
        url = f"/projects/{project_id}/bleachingqcs/sampleevents/"
        return self.data_frame_from_url(url)
