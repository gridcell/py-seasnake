from ..base import DataFrame, MermaidBase


class SampleEvent(MermaidBase):
    """
    The SampleEvent class is responsible for fetching summary information about sample events
    across various projects.
    """

    def summary(self, limit_columns: bool = True, flatten: bool = True) -> DataFrame:
        """
        Get a summary of sample events data from MERMAID.

        This method retrieves summary information about Sample Events and returns the result as
        a pandas DataFrame. By default, it limits the columns included in the DataFrame and
        flattens the `protocols` (or sample methods) column. However, these behaviors can be
        changed using the input parameters.

        Args:
            limit_columns (bool, optional): Whether to limit the columns included
            in the DataFrame. Defaults to True.
            flatten (bool, optional): Whether to flatten the 'protocols' column in
            the DataFrame. Defaults to True.

        Returns:
            DataFrame
        """
        columns = [
            "project",
            "tags",
            "country",
            "site",
            "latitude",
            "longitude",
            "reef_type",
            "reef_zone",
            "reef_exposure",
            "management",
            "sample_date",
            "data_policy_beltfish",
            "data_policy_benthiclit",
            "data_policy_benthicpit",
            "data_policy_benthicpqt",
            "data_policy_habitatcomplexity",
            "data_policy_bleachingqc",
            "project_notes",
            "site_notes",
            "management_notes",
            "contact_link",
            "protocols",
        ]
        column_rename_map = {
            "project_name": "project",
            "country_name": "country",
            "site_name": "site",
            "management_name": "management",
        }

        url = "/summarysampleevents/"
        df = self.data_frame_from_url(
            url,
            columns=columns if limit_columns else None,
            rename_columns=column_rename_map if limit_columns else None,
        )
        return self.flatten(df, "protocols") if flatten else df
