from typing import List, Optional, Union

from .base import DataFrame, MermaidBase


class Project(MermaidBase):
    """
    A class for handling MERMAID projects.

    The Project class is responsible for fetching and searching projects from MERMAID.
    It provides methods to list your projects and search all projects based on specified criteria.

    Attributes:
        PROJECT_STATUS_OPEN (int): The project status value representing open projects.
    """

    PROJECT_STATUS_OPEN = 90

    def my_projects(self) -> DataFrame:
        """
        Get a list of your projects.

        This method retrieves a list of your projects.

        Returns:
            DataFrame
        """
        url = "/projects/"
        return self.data_frame_from_url(url)

    def search_projects(
        self,
        name: Optional[str] = None,
        countries: Union[None, str, List[str]] = None,
        tags: Union[None, str, List[str]] = None,
        include_test_projects: bool = False,
    ) -> DataFrame:
        """
        Searches all MERMAID projects and filters results based on the specified criteria.

        Args:
            name (Optional[str], optional): A name or list of names to search for in
            projects. Defaults to None.
            countries (Union[None, str, List[str]], optional): A country to search for
            in projects. Defaults to None.
            tags (Union[None, str, List[str]], optional): A tag or list of tags to search
            for in projects. Defaults to None.
            include_test_projects (bool, optional): Whether to include test projects in
            the search results. Defaults to False.

        Returns:
            DataFrame
        """

        url = "/projects/"

        query_params = {"showall": "t"}
        if tags:
            query_params["tags"] = tags if isinstance(tags, str) else ",".join(tags)
        if not include_test_projects:
            query_params["status"] = str(self.PROJECT_STATUS_OPEN)

        df = self.data_frame_from_url(url, query_params=query_params)

        if name:
            raise NotImplementedError("Searching by name is not yet implemented.")
            # query_params["name"] = name
        if countries:
            raise NotImplementedError("Searching by country is not yet implemented.")
            # query_params["countries"] = countries

        return df
