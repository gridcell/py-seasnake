from .base import BaseSummary, DataFrame, requires_token


class FishBeltTransect(BaseSummary):
    @requires_token
    def observations(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's Fish Belt Transect observations.

        Args:
            project_id (str): The ID of the project for which to fetch
                Fish Belt Transect observations.

        Returns:
            DataFrame

        Examples:
        ```
        from seasnake import MermaidAuth, FishBeltTransect

        auth = MermaidAuth()
        fish_belt = FishBeltTransect(token=auth.get_token())
        project_id = "AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE"
        print(fish_belt.observations(project_id))
        ```
        """

        url = f"/projects/{project_id}/beltfishes/obstransectbeltfishes/"
        df = self.read_cache(url)
        return self.to_cache(url, self.data_frame_from_url(url)) if df is None else df

    @requires_token
    def sample_units(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's Fish Belt Transect observations aggregated by sample units.

        Args:
            project_id (str): The ID of the project for which to fetch
                Fish Belt Transect sample units.

        Returns:
            DataFrame

        Examples:
        ```
        from seasnake import MermaidAuth, FishBeltTransect

        auth = MermaidAuth()
        fish_belt = FishBeltTransect(token=auth.get_token())
        project_id = "AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE"
        print(fish_belt.sample_units(project_id))
        ```
        """

        url = f"/projects/{project_id}/beltfishes/sampleunits/"
        df = self.read_cache(url)
        return self.to_cache(url, self.data_frame_from_url(url)) if df is None else df

    @requires_token
    def sample_events(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's Fish Belt Transect observations aggregated by sample events.

        Args:
            project_id (str): The ID of the project for which to fetch
                Fish Belt Transect sample events.

        Returns:
            DataFrame

        Examples:
        ```
        from seasnake import MermaidAuth, FishBeltTransect

        auth = MermaidAuth()
        fish_belt = FishBeltTransect(token=auth.get_token())
        project_id = "AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE"
        print(fish_belt.sample_events(project_id))
        ```
        """

        url = f"/projects/{project_id}/beltfishes/sampleevents/"
        df = self.read_cache(url)
        return self.to_cache(url, self.data_frame_from_url(url)) if df is None else df
