{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# VacationPy\n",
    "----\n",
    "\n",
    "#### Note\n",
    "* Keep an eye on your API usage. Use https://developers.google.com/maps/reporting/gmp-reporting as reference for how to monitor your usage and billing.\n",
    "\n",
    "* Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'g_key'",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-1-744e1b5beb94>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mnumpy\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mnp\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mrequests\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 6\u001b[0;31m \u001b[0;32mimport\u001b[0m \u001b[0mg_key\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      7\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mos\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      8\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'g_key'"
     ]
    }
   ],
   "source": [
    "# Dependencies and Setup\n",
    "import matplotlib.pyplot as plt\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import requests\n",
    "import g_key\n",
    "import os\n",
    "\n",
    "# Import API key\n",
    "from api_keys import g_key"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Store Part I results into DataFrame\n",
    "* Load the csv exported in Part I to a DataFrame"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "city_data_df = pd.read_csv(\"output_data/cities.csv\")\n",
    "\n",
    "city_data_df.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Humidity Heatmap\n",
    "* Configure gmaps.\n",
    "* Use the Lat and Lng as locations and Humidity as the weight.\n",
    "* Add Heatmap layer to map."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#configure maps\n",
    "gmaps.configure(api_key=g_key)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#heatmap of humidity\n",
    "locations = city_data_df[[\"Lat\", \"Lng\"]]\n",
    "humidity = city_data_df[\"Humidity\"]\n",
    "fig = gmaps.figure()\n",
    "heat_layer = gmaps.heatmap_layer(locations, weights=humidity, dissipating=False, max_intensity=300, point_radius=5)\n",
    "\n",
    "fig.add_layer(heat_layer)\n",
    "fig"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Create new DataFrame fitting weather criteria\n",
    "* Narrow down the cities to fit weather conditions.\n",
    "* Drop any rows will null values."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "narrowed_city_df = city_data_df.loc[(city_data_df[\"Max Temp\"] < 80) & (city_data_df[\"Max Temp\"] > 70) \\\n",
    "                                    & (city_data_df[\"Wind Speed\"] < 10) \\\n",
    "                                    & (city_data_df[\"Cloudiness\"] == 0)].dropna()\n",
    "narrowed_city_df"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Hotel Map\n",
    "* Store into variable named `hotel_df`.\n",
    "* Add a \"Hotel Name\" column to the DataFrame.\n",
    "* Set parameters to search for hotels with 5000 meters.\n",
    "* Hit the Google Places API for each city's coordinates.\n",
    "* Store the first Hotel result into the DataFrame.\n",
    "* Plot markers on top of the heatmap."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#create a dataframe called hotel_df to hold hotel name and city\n",
    "hotel_df = narrowed_city_df[[\"City\", \"Country\", \"Lat\", \"Lng\"]].copy()\n",
    "hotel_df = [\"Hotel Name\"] = \"\"\n",
    "\n",
    "hotel_df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "params = {\n",
    "    \"radius\": 5000,\n",
    "    \"types\": \"lodging\",\n",
    "    \"key\": g_key\n",
    "    \n",
    "}\n",
    "\n",
    "#get lat and lng\n",
    "for index, row in hotel_df.iterrows():\n",
    "    lat = row[\"Lat\"]\n",
    "    lng = row[\"Lng\"]\n",
    "    \n",
    "    params[\"Location\"] = f\"{lat},{Lng}\"\n",
    "    \n",
    "    #use search terms hotel and our lat and lng\n",
    "    base_url = \"https://maps.googleapis.com/maps/api/place/nearbysearch/json\"\n",
    "    \n",
    "    name_address = requests.get(base_url, params=params).json()\n",
    "    \n",
    "    try:\n",
    "        hotel_df.loc[index, \"Hotel Name\"] = name_address[\"results\"][0][\"name\"]\n",
    "    except(KeyError, IndexError):\n",
    "        print(\"Missing field/Result...skipping\")\n",
    "hotel_df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# NOTE: Do not change any of the code in this cell\n",
    "\n",
    "# Using the template add the hotel marks to the heatmap\n",
    "info_box_template = \"\"\"\n",
    "<dl>\n",
    "<dt>Name</dt><dd>{Hotel Name}</dd>\n",
    "<dt>City</dt><dd>{City}</dd>\n",
    "<dt>Country</dt><dd>{Country}</dd>\n",
    "</dl>\n",
    "\"\"\"\n",
    "# Store the DataFrame Row\n",
    "# NOTE: be sure to update with your DataFrame name\n",
    "hotel_info = [info_box_template.format(**row) for index, row in hotel_df.iterrows()]\n",
    "locations = hotel_df[[\"Lat\", \"Lng\"]]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Add marker layer ontop of heat map\n",
    "\n",
    "\n",
    "# Display figure\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  },
  "latex_envs": {
   "LaTeX_envs_menu_present": true,
   "autoclose": false,
   "autocomplete": true,
   "bibliofile": "biblio.bib",
   "cite_by": "apalike",
   "current_citInitial": 1,
   "eqLabelWithNumbers": true,
   "eqNumInitial": 1,
   "hotkeys": {
    "equation": "Ctrl-E",
    "itemize": "Ctrl-I"
   },
   "labels_anchors": false,
   "latex_user_defs": false,
   "report_style_numbering": false,
   "user_envs_cfg": false
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
