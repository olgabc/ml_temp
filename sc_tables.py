import pandas as pd


class BigCSVTable:
    def __init__(
            self,
            file_names,
            dtype=None,
            usecols=None,
            date_cols=None,
            encoding=None,
    ):
        assert isinstance(file_names, list), "file_names is not a list"

        self.date_cols = date_cols
        dfs = []

        for file_name in file_names:
            df = pd.read_csv(
                file_name,
                sep=";",
                dtype=dtype,
                usecols=usecols,
                encoding=encoding,
            )
            dfs.append(df)

        self.df = pd.concat(dfs)
        self._dates_formated = False
        print(self.df)  # todelete

    def get_extra_dates(
            self,
            df_years=None,
            df_months=None,
            df_days=None,
            df_hours=None,
            df_dates=None,
            df_daysofweek=None,
            df_days_delta=None,
            df_time_delta=None,
          ):
        """

        :param df_years:
        :param df_months:
        :param df_days:
        :param df_hours:
        :param df_dates:
        :param df_daysofweek:
        :param df_days_delta: tuple(earlier date, last_date)
        :param df_time_delta: tuple(earlier date, last_date)
        :return:
        """
        assert df_days_delta is None or (
                isinstance(df_days_delta, tuple) and len(df_days_delta) == 2
        ), "check days_delta"

        assert df_time_delta is None or (
                isinstance(df_time_delta, tuple) and len(df_time_delta) == 2
        ), "check time_delta"

        df_dates_cols = [df_years, df_months, df_days, df_hours, df_dates, df_daysofweek, df_days_delta, df_time_delta]
        df_date_cols = []

        for df_dates_col in df_dates_cols:
            if df_dates_col:
                df_date_cols += df_dates_col

        df_date_cols = set(df_date_cols)

        for df_date_col in df_date_cols:
            self.df[df_date_col] = pd.to_datetime(
                self.df[df_date_col],
                dayfirst=True
            )

        if df_years:
            for date_col in df_years:
                self.df["{}_YEAR".format(date_col)] = self.df[date_col].dt.year

        if df_months:
            for date_col in df_months:
                self.df["{}_MONTH".format(date_col)] = self.df[date_col].dt.month

        if df_days:
            for date_col in df_days:
                self.df["{}_DAY".format(date_col)] = self.df[date_col].dt.day

        if df_hours:
            for date_col in df_hours:
                self.df["{}_HOUR".format(date_col)] = self.df[date_col].dt.hour

        if df_dates:
            for date_col in df_dates:
                self.df["{}_DATE".format(date_col)] = self.df[date_col].dt.date

        if df_daysofweek:
            for date_col in df_daysofweek:
                self.df["{}_DAYOFWEEK".format(date_col)] = self.df[date_col].dt.dayofweek
                self.df["{}_DAYOFWEEK".format(date_col)] = self.df["{}_DAYOFWEEK".format(date_col)] + 1

        if df_days_delta:
            for num in (0,1):
                try:
                    self.df["{}_DATE".format(df_days_delta[num])]
                except KeyError:
                    self.df["{}_DATE".format(df_days_delta[num])] = self.df[df_days_delta[num]].dt.date

            self.df["{}-{}(DATES)".format(
                df_days_delta[1],
                df_days_delta[0]
            )] = self.df["{}_DATE".format(df_days_delta[1])] - self.df["{}_DATE".format(df_days_delta[0])]
            print((
                self.df["{}_DATE".format(df_days_delta[0])], self.df["{}_DATE".format(df_days_delta[1])]
            ))
            self.df["{}-{}(DATES)".format(
                df_days_delta[1],
                df_days_delta[0]
            )] = self.df["{}-{}(DATES)".format(
                df_days_delta[1],
                df_days_delta[0]
            )].dt.days
        
        if df_time_delta:
            self.df["{}-{}(TIME)".format(df_time_delta[1], df_time_delta[0])] = self.df[df_time_delta[1]] - self.df[df_time_delta[0]]
            self.df["{}-{}(TIME)".format(
                df_time_delta[1],
                df_time_delta[0]
            )] = self.df["{}-{}(TIME)".format(df_time_delta[1], df_time_delta[0])].dt.seconds / 60
