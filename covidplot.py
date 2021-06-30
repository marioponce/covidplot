# -*- coding: utf-8 -*-
"""Classes to plot the covid cases of a specific country. 
Code by Mario Ponce (June, 2021)
"""
import pandas as pd # To manage to datasets
import plotly.express as px # To plot the spatial data

def myCaps(id_):
    """Returns an id according to the list of available countries

    args:
      id_ [string]

    output:
      string with the first letter of each word of id_ capitalized
      except "and", "the"
    """
    exceptions = ["and", "the"]
    # converts id into a list
    particles = id_.split()
    particles = [p.capitalize() if p not in exceptions else p for p in particles ]
    np = len(particles)
    # re-doing the string
    id_ = ""
    i = 1
    for p in particles:
        id_ += p
        if i < np:
            id_ += " "
            i+=1
    # dealing with "-" cases
    if "-" in id_:
        toCap = id_.index("-") + 1
        id_ = id_[:toCap] + id_[toCap].upper() + id_[toCap+1:]
    # dealing with "'" cases
    elif "'" in id_:
        toCap = id_.index("'") + 1
        id_ = id_[:toCap-2] + id_[toCap-2].lower() + "'" + id_[toCap].upper() + id_[toCap+1:]
    # special cases
    elif id_ in ["Us"]:
        id_ = id_.upper()

    return id_

class Connector:
    """Class for getting data from covid-api as a dict

    Attributes:
      url [str] : query url that maches with the request country
      d [dict] : downloaded data
    """
    def __init__(self, country):
        """Class constructor

        args:
          country [string]

        output:
          None
        """
        url_base ="https://covid-api.mmediagroup.fr/v1/cases"
        valid_input = True # a flag to evaluet the input
        countries = list(pd.read_json(url_base).keys())
        if not isinstance(country, str): # if the input is not a str
            valid_input = False
        else:
            country = myCaps(country)
            # if the input is an empty str or it is not on the list of countries
            if country == "" or not country in countries:
                valid_input = False
            # dealing with spaces
            country = country.replace(" ", "%20")
        # if the input is valid then let's do the query
        if valid_input:
            self.url = url_base + "?country=" + country
            self.d = pd.read_json(self.url)
            pd.read_json("https://covid-api.mmediagroup.fr/v1/cases")
        else:
            self.url = ""
            self.d = None
            print("No valid input. You could try:")
            # showing the possible valid inputs
            for c in countries:
                print("    " + c)

class CovidPlotter(Connector):
    """Class to request and plot the covid cases for country

    Attributes:
      url [str] : query url that maches with the request country
      d [dict] : downloaded data
      df [DataFrame] : structured downloaded data

    Funtions:
      plot

    Protected functions:
      __dict2df
    """
    def __init__(self, country):
        """Class constructor

        This constructor is inherited from the class Connector
        args:
          country [string]

        output:
          None
        """

        # calling the constructor of the class Connector
        Connector.__init__(self, country)
        # converting the data in the format requested by the plotting
        try:
            self.__dict2df()
        except:
            print("Please check the input")
    def __dict2df(self):
        """Convert the downloaded data into a DataFrame

        args:
          None

        output:
          None
        """
        # using List Comprehesion to filter the list of provinces
        province = [k for k in self.d.keys() if k!="Unknown"]
        # initializing the field of the DataFrame
        confirmed = []
        recovered = []
        deaths = []
        lat = []
        lon = []
        # filling the DataFrame from the dict
        for p in province:
            confirmed.append(self.d[p]["confirmed"])
            recovered.append(self.d[p]["recovered"])
            deaths.append(self.d[p]["deaths"])
            lat.append(float(self.d[p]["lat"]))
            lon.append(float(self.d[p]["long"]))
        # This dict contains the same data but it is structured by flieds
        # before this the info was structured as a tree
        d = {"province": province, "confirmed": confirmed,
             "recovered": recovered, "deaths": deaths,
             "lat":lat, "lon":lon}
        # Creating the DataFrame
        self.df = pd.DataFrame(data=d)
    def plot(self):
        """Plots the geo-spatial data in a interactive canvas

        args:
          None

        output:
          None
        """
        try:
            # Setting the DataFrame's info up
            fig = px.scatter_mapbox(self.df, lat="lat", lon="lon",
                                    hover_name="province",
                                    hover_data=["confirmed", "recovered", "deaths"],
                            color_discrete_sequence=["fuchsia"], zoom=3, height=300)
            fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            fig.show()
        except:
            print("Impossible to plot. Please, check the instance.")
