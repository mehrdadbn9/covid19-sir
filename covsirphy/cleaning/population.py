#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from covsirphy.cleaning.cbase import CleaningBase


class Population(CleaningBase):
    """
    Data cleaning of total population dataset.
    """

    def __init__(self, filename):
        super().__init__(filename)

    def cleaning(self):
        """
        Perform data cleaing of the raw data.
        This method overwrite super().cleaning() method.
        @return <pd.DataFrame>
            - Country <str>: country/region name
            - Province <str>: province/prefecture/state name
            - Population <int>: total population
        """
        df = self._raw.copy()
        # Rename the columns
        df = df.rename(
            {
                "Country.Region": self.COUNTRY,
                "Province.State": self.PROVINCE,
                "Population": self.N
            },
            axis=1
        )
        # Country
        df[self.COUNTRY] = df[self.COUNTRY].replace(
            {
                "Mainland China": "China",
                "Hong Kong SAR": "Hong Kong",
                "Taipei and environs": "Taiwan",
                "Iran (Islamic Republic of)": "Iran",
                "Republic of Korea": "South Korea",
                "Republic of Ireland": "Ireland",
                "Macao SAR": "Macau",
                "Russian Federation": "Russia",
                "Republic of Moldova": "Moldova",
                "Taiwan*": "Taiwan",
                "Cruise Ship": "Others",
                "United Kingdom": "UK",
                "Viet Nam": "Vietnam",
                "Czechia": "Czech Republic",
                "St. Martin": "Saint Martin",
                "Cote d'Ivoire": "Ivory Coast",
                "('St. Martin',)": "Saint Martin",
                "Congo (Kinshasa)": "Congo",
                "Congo (Brazzaville)": "Congo",
                "The, Bahamas": "Bahamas",
            }
        )
        # Province
        df[self.PROVINCE] = df[self.PROVINCE].fillna("-").replace(
            {
                "Cruise Ship": "Diamond Princess",
                "Diamond Princess cruise ship": "Diamond Princess"
            }
        )
        df.loc[df[self.COUNTRY] == "Diamond Princess", [
            self.COUNTRY, self.PROVINCE]] = ["Others", "Diamond Princess"]
        # Values
        df[self.N] = df[self.N].astype(np.int64)
        df = df.loc[:, [self.COUNTRY, self.PROVINCE, self.N]]
        return df

    def total(self):
        """
        Return the total value of population in the datset.
        @return <int>
        """
        values = self._cleaned_df[self.N]
        return sum(values)

    def to_dict(self, country_level=True):
        """
        Return dictionary of population values.
        @country_level <str>: whether key is country name or not
        @return <dict[str]=int>:
            - if @country_level is True, {"country", population}
            - if False, {"country/province", population}
        """
        df = self._cleaned_df.copy()
        if country_level:
            df = df.loc[df[self.PROVINCE] == "-", :]
            df["key"] = df[self.COUNTRY]
        else:
            df["key"] = df[self.COUNTRY].str.cat(df[self.PROVINCE], sep="/")
        pop_dict = df.set_index("key").to_dict()[self.N]
        return pop_dict
