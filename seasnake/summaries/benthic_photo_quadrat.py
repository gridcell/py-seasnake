from .base import BaseSummary, DataFrame, requires_token


class BenthicPhotoQuadrat(BaseSummary):
    """
    A class for handling Benthic Photo Quadrat data from MERMAID.

    The BenthicPhotoQuadrat class is responsible for fetching Benthic Photo Quadrat data,
    including observations, observations aggregated by sample units, and observations
    aggregated by sample events, for a specified project.
    """

    @requires_token
    def observations(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's Benthic Photo Quadrat observations.

        Args:
            project_id (str): The ID of the project for which to fetch
                Benthic Photo Quadrat observations.

        Returns:
            DataFrame

        Examples:
        ```
        from seasnake import MermaidAuth, BenthicPhotoQuadrat

        auth = MermaidAuth()
        bpq = BenthicPhotoQuadrat(token=auth.get_token())
        project_id = "AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE"
        print(bpq.observations(project_id))
        ```
        """

        url = f"/projects/{project_id}/benthicpqts/obstransectbenthicpqts/"
        df = self.read_cache(url)
        return self.to_cache(url, self.data_frame_from_url(url)) if df is None else df

    @requires_token
    def sample_units(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's Benthic Photo Quadrat observations aggregated by sample units.

        Args:
            project_id (str): The ID of the project for which to fetch
                Benthic Photo Quadrat sample units.

        Returns:
            DataFrame

        Examples:
        ```
        from seasnake import MermaidAuth, BenthicPhotoQuadrat

        auth = MermaidAuth()
        bpq = BenthicPhotoQuadrat(token=auth.get_token())
        project_id = "AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE"
        print(bpq.sample_units(project_id))
        ```
        """

        url = f"/projects/{project_id}/benthicpqts/sampleunits/"
        df = self.read_cache(url)
        return self.to_cache(url, self.data_frame_from_url(url)) if df is None else df

    @requires_token
    def sample_events(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's Benthic Photo Quadrat observations aggregated by sample events.

        Args:
            project_id (str): The ID of the project for which to fetch
                Benthic Photo Quadrat sample events.

        Returns:
            DataFrame

        Examples:
        ```
        from seasnake import MermaidAuth, BenthicPhotoQuadrat

        auth = MermaidAuth()
        bpq = BenthicPhotoQuadrat(token=auth.get_token())
        project_id = "AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE"
        print(bpq.sample_events(project_id))
        ```
        """

        url = f"/projects/{project_id}/benthicpqts/sampleevents/"
        df = self.read_cache(url)
        return self.to_cache(url, self.data_frame_from_url(url)) if df is None else df
