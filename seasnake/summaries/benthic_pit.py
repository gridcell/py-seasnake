from .base import BaseSummary, DataFrame, requires_token


class BenthicPIT(BaseSummary):
    """
    A class for handling Benthic Point Intercept Transect (PIT) data from MERMAID.

    The BenthicPIT class is responsible for fetching Benthic PIT data, including observations,
    observations aggregated by sample units, and observations aggregated by sample events,
    for a specified project.
    """

    @requires_token
    def observations(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's Benthic PIT observations.

        Args:
            project_id (str): The ID of the project for which to fetch Benthic PIT observations.

        Returns:
            DataFrame

        Examples:
        ```
        from seasnake import MermaidAuth, BenthicPIT

        auth = MermaidAuth()
        benthic_pit = BenthicPIT(token=auth.get_token())
        project_id = "AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE"
        print(benthic_pit.sample_events(project_id))
        ```
        """
        url = f"/projects/{project_id}/benthicpits/obstransectbenthicpits/"
        df = self.read_cache(url)
        return self.to_cache(url, self.data_frame_from_url(url)) if df is None else df

    @requires_token
    def sample_units(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's Benthic PIT observations aggregated by sample units.

        Args:
            project_id (str): The ID of the project for which to fetch Benthic PIT sample units.

        Returns:
            DataFrame
        Examples:
        ```
        from seasnake import MermaidAuth, BenthicPIT

        auth = MermaidAuth()
        benthic_pit = BenthicPIT(token=auth.get_token())
        project_id = "AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE"
        print(benthic_pit.sample_events(project_id))
        ```
        """

        url = f"/projects/{project_id}/benthicpits/sampleunits/"
        df = self.read_cache(url)
        return self.to_cache(url, self.data_frame_from_url(url)) if df is None else df

    @requires_token
    def sample_events(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's Benthic PIT observations aggregated by sample events.

        Args:
            project_id (str): The ID of the project for which to fetch Benthic PIT sample events.

        Returns:
            DataFrame

        Examples:
        ```
        from seasnake import MermaidAuth, BenthicPIT

        auth = MermaidAuth()
        benthic_pit = BenthicPIT(token=auth.get_token())
        project_id = "AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE"
        print(benthic_pit.sample_events(project_id))
        ```
        """

        url = f"/projects/{project_id}/benthicpits/sampleevents/"
        df = self.read_cache(url)
        return self.to_cache(url, self.data_frame_from_url(url)) if df is None else df
